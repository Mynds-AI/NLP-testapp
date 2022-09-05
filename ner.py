import spacy


def getner(sentence):
    nlp_ner = spacy.load("ner_output/model-best")

    result = []

    for ent in nlp_ner(sentence).ents:
        result.append((ent.text, ent.label_))

    return result


def get_location(sentence):
    nlp = spacy.load("hu_core_news_lg")
    doc = nlp(sentence)

    result = []

    for ent in doc.ents:
        if ent.label_ == "LOC":
            result.append(ent.lemma_)

    return result
