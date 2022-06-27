import spacy
from spacy.tokens import DocBin


def make_docs():
    nlp = spacy.load("hu_core_news_lg")
    # the DocBin will store the example documents
    db = DocBin()
    training_data = [
        (
        "A feleségemmel Rómában ismerkedtünk meg. Az évfordulóra szeretnék rendelni egy Róma térképet a nevünkkel, szépen becsomagolva, hogy már csak át kelljen adnom.",
        [(2, 14, "GENDERROLE"), (44, 55, "OCCASION"), (84, 92, "PRODUCT")]),
        ("Rendelek egy nagy arany rózsamacit. Érkezhet már eleve díszcsomagolásban, megcímzett kártyával.",
         [(24, 34, "PRODUCT"), (13, 17, "PRODUCTSIZE"), (18, 23, "PRODUCTCOLOR")]),
        (
        "Rendelni szeretnék egy szál piros örökrózsát piros szívvel, Pétertől Katinak címzett kártyával. Egyszerű csomagolás elég lesz.",
        [(34, 44, "PRODUCT"), (28, 33, "PRODUCTCOLOR")]),
        ("Holnapután Valentin nap. Kérlek, küldjetek bármi rózsaszín ajándékot a barátnőmnek 10-15 ezer forint körül.",
         [(11, 23, "OCCASION"), (49, 58, "PRODUCTCOLOR"), (71, 82, "GENDERROLE")]),
        (
        "Tegnap rendeltem egy zöld nagy méretű rózsamacit, viszont praktikusabb lenne, ha a közepes méretűből vennék rózsaszínt. Örülnék, ha módosítani tudnátok a rendelésemet.",
        [(38, 48, "PRODUCT"), (21, 25, "PRODUCTCOLOR"), (26, 30, "PRODUCTSIZE"), (83, 90, "PRODUCTSIZE"),
         (108, 118, "PRODUCTCOLOR")]),
    ]
    for text, annotations in training_data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk("./ner_data/ner_valid.spacy")


if __name__ == "__main__":
    make_docs()


# test_docs, test_data = make_docs()
# # then we save it in a binary file to disc
# doc_bin = DocBin(docs=test_docs)
# doc_bin.to_disk("./ner_data/ner_valid.spacy")
