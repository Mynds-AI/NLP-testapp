import datetime
import numerizer
from string import punctuation

import spacy

nlp_hu = spacy.load("hu_core_news_lg")
nlp_en = spacy.load("en_core_web_md")


def get_hotwords(text, lng):
    if lng == 'hu':
        doc = nlp_hu(text.lower() + ".")
        i18n_quantity_distance = ["méter", "kilóméter", "km"]
        i18n_district = "kerület"
        i18n_open = "nyitva"
    elif lng == 'en':
        doc = nlp_en(text.lower() + ".")
        i18n_quantity_distance = ["meter", "kilometer" "km"]
        i18n_district = "district"
        i18n_open = "open"

    result = []
    pos_tag = ['ADJ', 'NOUN']
    continue_again = False
    for token in doc:
        if token.text in (nlp_hu.Defaults.stop_words if lng == 'hu' else nlp_en.Defaults.stop_words) or token.text in punctuation:
            continue
        elif any(ext in token.lemma_ for ext in i18n_quantity_distance):
            continue
        if continue_again:
            continue_again = False
            continue

        if token.pos_ in pos_tag:
            if doc[token.i + 1].lemma_ == i18n_district:
                continue
            if i18n_district in token.lemma_:
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
        if i18n_open in tok.lemma_ or i18n_quantity_distance[0] in tok.lemma_:
            for text in result:
                if doc[tok.i + 1].text in text or doc[tok.i + 1].lemma_ in text:
                    result.remove(text)
                    continue
                if doc[tok.i - 1].text in text or doc[tok.i - 1].lemma_ in text:
                    result.remove(text)
                    continue

    return set(list(filter(str.strip, result)))


def get_time(text, lng):
    if lng == 'hu':
        doc = nlp_hu(text)
        i18n_open = "nyitva"
    elif lng == 'en':
        doc = nlp_en(text)
        i18n_open = "open"
    result = ""
    for token in doc:
        if i18n_open in token.lemma_:
            try:
                result = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%H:%M:%S")
                continue
            except:
                continue
    return result


def get_radius(text, lng):
    if lng == 'hu':
        doc = nlp_hu(text)
        i18n_quantity_distance = ["méter", "kilóméter", "km"]
        i18n_quantity_m = "méter"
        i18n_quantity_km = "kilóméter"
    elif lng == 'en':
        doc = nlp_en(text)
        i18n_quantity_distance = ["meter", "kilometer" "km"]
        i18n_quantity_m = "meter"
        i18n_quantity_km = "kilometer"

    result = ""
    for token in doc:
        if any(ext in token.lemma_ for ext in i18n_quantity_distance):
            try:
                distance_quantity = int(doc[token.i - 1].lemma_)
                result = str(distance_quantity) + " " + token.lemma_
                continue
            except:
                continue
    return result

