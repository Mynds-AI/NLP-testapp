import spacy
from spacy.tokens import DocBin

import spreadsheet_handler


def make_docs(type):
    file = "./ner_data/ner_train.spacy" if type == "train" else "./ner_data/ner_valid.spacy"
    sheet_type = "ner_training" if type == "train" else "ner_valid"

    nlp = spacy.load("hu_core_news_lg")
    db = DocBin()
    training_datas = spreadsheet_handler.get_ner_sentences(sheet_type)
    for data in training_datas:
        text = eval(data[0])[0]
        annotations = eval(data[0])[1]
        doc = nlp(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(file)


make_docs(type="train")

make_docs(type="valid")

