import json

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

    paramNames = ner.getner(json.loads(request.data)['entityString'])

    result = "Elsődleges szándék: " + \
             textcat.getcat(json.loads(request.data)['entityString']) + ", paraméter név: " + str(paramNames).strip('[]') + \
             ", paraméter érték: " + ', '.join(params)
    return result


app.run()
