import datetime
from string import punctuation

import spacy

nlp = spacy.load("hu_core_news_lg")


def get_hotwords(text):
    result = []
    pos_tag = ['ADJ', 'NOUN']
    doc = nlp(text.lower() + ".")
    continue_again = False
    for token in doc:
        if token.text in nlp.Defaults.stop_words or token.text in punctuation:
            continue
        elif token.lemma_ == "méter" or token.lemma_ == "kilóméter":
            continue
        if continue_again:
            continue_again = False
            continue

        if token.pos_ in pos_tag:
            if doc[token.i + 1].lemma_ == "kerület":
                continue
            if "kerület" in token.lemma_:
                result.append(doc[token.i - 1].lemma_ + " " + token.lemma_)
                continue
            if token.dep_ == "amod:att":
                result.append(token.lemma_ + " " + doc[token.i + 1].lemma_)
                continue_again = True
                continue
            if len(result) > 1 and token.lemma_ in result[-1]:
                continue
            result.append(token.lemma_)

    for tok in doc:
        if "nyitva" in tok.lemma_ or "méter" in tok.lemma_:
            for text in result:
                if doc[tok.i + 1].text in text or doc[tok.i + 1].lemma_ in text:
                    result.remove(text)
                if doc[tok.i - 1].text in text or doc[tok.i - 1].lemma_ in text:
                    result.remove(text)

    return list(filter(str.strip, result))


def get_time(text):
    doc = nlp(text)
    result = ""
    for token in doc:
        if "nyitva" in token.lemma_:
            try:
                result = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%H:%M:%S")
                continue
            except:
                continue
    return result


def get_radius(text):
    doc = nlp(text)
    result = ""
    for token in doc:
        if "méter" in token.lemma_ or "kilóméter" in token.lemma_:
            try:
                distance_quantity = int(doc[token.i - 1].lemma_)
                result = str(distance_quantity) + " " + token.lemma_
                continue
            except:
                continue
    return result

