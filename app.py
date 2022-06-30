import json
import io
import csv

import flask

import textcat
import ner
import keyword_extractor
from flask import request, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def getmaintemplate():
    return render_template('index.html')


@app.route('/getcat', methods=['POST'])
def getcat():

    params = keyword_extractor.get_hotwords(json.loads(request.data)['entityString'])

    result = dict()

    result['primary_intent'] = textcat.getcat(json.loads(request.data)['entityString'])
    result['param_name'] = ner.getner(json.loads(request.data)['entityString'])
    result['param_value'] = ', '.join(params)

    return result


@app.route('/runallsentence', methods=['GET'])
def runallsentence():

    allsentences = io.open('allsentences.txt', mode="r", encoding="utf-8")
    sentences = allsentences.readlines()

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

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


app.run()
