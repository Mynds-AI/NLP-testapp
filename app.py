import json
import csv
import re
from flask_cors import CORS, cross_origin
import spreadsheet_handler

import flask

import textcat
import ner
import keyword_extractor
from flask import request, render_template, send_file

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def get_main_template():
    return render_template('index.html')


@app.route('/getintent', methods=['POST'])
@cross_origin()
def get_intent():

    params = keyword_extractor.get_hotwords(json.loads(request.data)['entityString'])

    result = dict()

    result['primary_intent'] = textcat.getcat(json.loads(request.data)['entityString'])
    result['param_name'] = ner.getner(json.loads(request.data)['entityString'])
    result['param_value'] = ', '.join(params)

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


app.run()

