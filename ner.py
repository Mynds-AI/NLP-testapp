import spacy


def getner(sentence):
    nlp_ner = spacy.load("ner_output/model-best")

    result = []

    for ent in nlp_ner(sentence).ents:
        result.append((ent.text, ent.label_))

    return result
