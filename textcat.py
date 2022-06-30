import spacy


def getcat(sentence):
    nlp_textcat = spacy.load("textcat_output/model-best")

    result = dict()
    result['intent'] = dict()
    result['other_intent'] = []
    other_intent = dict()

    doc = nlp_textcat(sentence)
    if doc.cats['information'] >.5:
        result['intent']['intent_name'] = 'information'
        result['intent']['intent_percentage'] = "{:.2%}".format((doc.cats['information']))
        for cat in doc.cats:
            if cat != 'information':
                other_intent['name'] = cat
                other_intent['percentage'] = "{:.2%}".format(doc.cats[cat])
                other_intent_copy = other_intent.copy()
                result['other_intent'].append(other_intent_copy)
        return result
    elif doc.cats['order'] >.5:
        result['intent']['intent_name'] = 'order'
        result['intent']['intent_percentage'] = "{:.2%}".format((doc.cats['order']))
        for cat in doc.cats:
            if cat != 'order':
                other_intent['name'] = cat
                other_intent['percentage'] = "{:.2%}".format(doc.cats[cat])
                other_intent_copy = other_intent.copy()
                result['other_intent'].append(other_intent_copy)
        return result
    elif doc.cats['order_modification'] > .5:
        result['intent']['intent_name'] = 'order_modification'
        result['intent']['intent_percentage'] = "{:.2%}".format((doc.cats['order_modification']))
        for cat in doc.cats:
            if cat != 'order_modification':
                other_intent['name'] = cat
                other_intent['percentage'] = "{:.2%}".format(doc.cats[cat])
                other_intent_copy = other_intent.copy()
                result['other_intent'].append(other_intent_copy)
        return result
    elif doc.cats['complaint'] > .5:
        result['intent']['intent_name'] = 'complaint'
        result['intent']['intent_percentage'] = "{:.2%}".format((doc.cats['complaint']))
        for cat in doc.cats:
            if cat != 'complaint':
                other_intent['name'] = cat
                other_intent['percentage'] = "{:.2%}".format(doc.cats[cat])
                other_intent_copy = other_intent.copy()
                result['other_intent'].append(other_intent_copy)
        return result
    else:
        return "unknown intent"

