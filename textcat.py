import spacy


def getcat(sentence):
    nlp_textcat = spacy.load("textcat_output/model-best")

    doc = nlp_textcat(sentence)
    if doc.cats['information'] >.5:
        return "information"
    elif doc.cats['order'] >.5:
        return "order"
    elif doc.cats['order_modification'] > .5:
        return "order_modification"
    elif doc.cats['complaint'] > .5:
        return "complaint"

