import spacy

nlp_hu = spacy.load("hu_core_news_lg")
nlp_en = spacy.load("en_core_web_md")

def getner(sentence):
    nlp_ner = spacy.load("ner_output/model-best")

    result = []

    for ent in nlp_ner(sentence).ents:
        result.append((ent.text, ent.label_))

    return result


def get_location(sentence, lng):
    if lng == 'hu':
        doc = nlp_hu(sentence)
    elif lng == 'en':
        doc = nlp_en(sentence)

    result = []
    for ent in doc.ents:
        if ent.label_ == "LOC" or ent.label_ == "GPE":
            result.append(ent.lemma_)

    return result


def get_organisation(text, lng):
    if lng == 'hu':
        doc = nlp_hu(text)
    elif lng == 'en':
        doc = nlp_en(text)
    result = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            result.append(ent.lemma_)

    return result
