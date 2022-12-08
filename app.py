import json
import csv
import re

from flasgger import LazyJSONEncoder, LazyString, Swagger, swag_from
from flask_cors import CORS, cross_origin

import spreadsheet_handler
import myndsai_logger

import flask

import textcat
import ner
import keyword_extractor
from flask import request, render_template, send_file

app = flask.Flask(__name__)
app.json_encoder = LazyJSONEncoder
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SWAGGER'] = {
    'title': 'MyndsAI NLP API Documentation',
    'uiversion': 3
}

swagger_template = dict(
    info={
        'title': LazyString(lambda: 'MyndsAI NLP HU-EN application'),
        'version': LazyString(lambda: '1.0'),
        'description': LazyString(lambda: ''),
        },
    host=LazyString(lambda: request.host)
)


swagger = Swagger(app, template=swagger_template)


@app.route('/getintent', methods=['POST'])
@cross_origin()
def get_intent():
    """With the given required entityString and the optional lng parameter a language process will go through on the users input and the result will be sent back or will be displayed on the screen.
    For getting the primary_intent and the param_name properties the own-trained language model is going to be used which
    has been trained especially for the voicebot of rosebear webshop. All other parameters will be extracted by the hungarian
    or english spacy core model.
    ---
    parameters:
      - name: entityString
        in: body
        type: string
        required: true
        default: éttermet keresek Budapesten a Benczúr utca 2 km es körzetében
      - name: lng
        in: body
        type: string
        required: false
        default: hu
    definitions:
      Result:
        type: object
        properties:
          locations:
            type: string
          organisations:
            type: string
          param_name:
            type: string
          param_value:
            type: string
          primary_intent:
            type: object
            $ref: '#/definitions/PrimaryIntent'
          radius:
            type: string
          time:
            type: string
      PrimaryIntent:
        type: object
        properties:
          intent:
            type: object
            $ref: '#/definitions/Intent'
          other_intent:
            type: array
            items:
              $ref: '#/definitions/Intent'
      Intent:
        type: object
        properties:
          intent_name:
            type: string
          intent_percentage:
            type: string
    responses:
      200:
        description: A result object of the language-processed sentence
        schema:
          $ref: '#/definitions/Result'
    """

    lng = 'hu'

    try:
        if json.loads(request.data)['lng'] is not None:
            lng = json.loads(request.data)['lng']
    except KeyError:
        pass

    message = {"lng": lng, "entityString": json.loads(request.data)['entityString']}

    myndsai_logger.send_log(request.base_url, json.dumps(message), "nlp_testapp", "info",
                            "intent_recognition_request_received")

    params = keyword_extractor.get_hotwords(json.loads(request.data)['entityString'], lng)

    result = dict()

    result['primary_intent'] = textcat.getcat(json.loads(request.data)['entityString'])
    result['param_name'] = ner.getner(json.loads(request.data)['entityString'])
    result['param_value'] = ', '.join(params)
    raw_locations = ner.get_location(json.loads(request.data)['entityString'], lng)

    splitted_locations = []

    for location in raw_locations:
        splitted_locations += location.split()

    for splitted_location in splitted_locations:
        result['param_value'] = result['param_value'].replace(splitted_location.lower(), "")

    result['locations'] = str(raw_locations) if len(raw_locations) > 0 else ""

    raw_organisations = ner.get_organisation(json.loads(request.data)['entityString'], lng)

    splitted_organisations = []

    for organisation in raw_organisations:
        splitted_organisations += organisation.split()

    for splitted_organisation in splitted_organisations:
        result['param_value'] = result['param_value'].replace(splitted_organisation.lower(), "")

    result['organisations'] = str(raw_organisations) if len(raw_organisations) > 0 else ""
    result['time'] = keyword_extractor.get_time(json.loads(request.data)['entityString'], lng)
    result['radius'] = keyword_extractor.get_radius(json.loads(request.data)['entityString'], lng)

    myndsai_logger.send_log(request.base_url, json.dumps(result), "nlp_testapp", "info",
                            "intent_recognition_request_sent")

    return result


@app.route('/create-ner-sentence', methods=['POST'])
def create_ner_sentence():

    ner_sentence = json.loads(request.data)['nerSentence']
    entities = [tuple(x.split('-')) for x in json.loads(request.data)['entities'].split(', ')]

    result = [ner_sentence]
    entity_list = []

    for tup in entities:
        entity_details = []
        for match in re.finditer(tup[0], ner_sentence):
            entity_details.append(match.regs[0][0])
            entity_details.append(match.regs[0][1])
            entity_details.append(tup[1])
        entity_list.append(tuple(entity_details))
    result.append(entity_list)

    spreadsheet_handler.append_row("ner_training", [[str(tuple(result))]])


@app.route('/runallsentence', methods=['GET'])
def runallsentence():

    sentences = spreadsheet_handler.get_all_sentences("text_classifier_training")

    with open('result.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)

        header = ['értékelt mondat', 'elsődleges szándék név', 'elsődleges szándék érték', 'paraméter név',
                   'paraméter érték', 'többi szándék']

        writer.writerow(header)

        for sentence in sentences:

            params = keyword_extractor.get_hotwords(sentence)

            paramNames = ner.getner(sentence)

            data = [sentence, textcat.getcat(sentence)['intent']['intent_name'], textcat.getcat(sentence)['intent']['intent_percentage'],
                    paramNames, params, textcat.getcat(sentence)['other_intent']]

            writer.writerow(data)

    return send_file("result.csv", as_attachment=True, download_name="result.csv")


@app.route('/test', methods=['GET'])
def test():
    sentences = spreadsheet_handler.get_all_sentences("text_classifier_training")

    params = keyword_extractor.get_hotwords(sentences[0])

    paramNames = ner.getner(sentences[0])

    data = [sentences[0], textcat.getcat(sentences[0])['intent']['intent_name'],
            textcat.getcat(sentences[0])['intent']['intent_percentage'],
            paramNames, params, textcat.getcat(sentences[0])['other_intent']]

    return str(data)


@app.route('/')
def get_main_template():
    return render_template('index.html')


app.run()

