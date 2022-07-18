from _csv import reader, writer

import spacy
import re
import pandas as pd
import string

from tqdm.auto import tqdm
from spacy.tokens import DocBin
from random import randrange, sample

import spreadsheet_handler


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def add_doublequote(text):
    if"," in text:
        quoted_text = '"{}"'.format(text)
        return quoted_text


def remove_url(text):
    url_pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return url_pattern.sub(r'', text)


def clean_text(text):
    delete_dict = {sp_character: '' for sp_character in string.punctuation}
    delete_dict[' '] = ' '
    table = str.maketrans(delete_dict)
    text1 = text.translate(table)
    textArr = text1.split()
    text2 = ' '.join([w for w in textArr if (not w.isdigit() and (not w.isdigit() and len(w) > 3))])

    return text2.lower()


def weight_sentences(type):
    randomised_list = []

    file_name = "train_weight.csv" if type == "train" else "valid_weight.csv"


    with open(file_name, 'w', encoding='utf-8', newline='') as writer_obj:
        csv_writer = writer(writer_obj)
        csv_writer.writerow(["textID", "text", "information_about"])
        for row in train_data:
            for x in range(0, int(row[3])):
                randomised_list.insert(randrange(len(randomised_list) + 1), [row[0], row[1], row[2]])
    for elem in randomised_list:
        csv_writer.writerow(elem)


def make_docs(type):

    sheet_type = "text_classifier_training" if type == "train" else "text_classifier_valid"
    file_name = spreadsheet_handler.create_textcat_sentences(sheet_type)

    train_data = pd.read_csv(file_name)
    train_data.dropna(axis=0, how='any', inplace=True)
    train_data['Num_words_text'] = train_data['text'].apply(lambda x: len(str(x).split()))
    mask = train_data['Num_words_text'] > 2
    train_data = train_data[mask]

    train_data['text'] = train_data['text'].apply(remove_emoji)
    train_data['text'] = train_data['text'].apply(remove_url)
    train_data['text'] = train_data['text'].apply(clean_text)

    data = tuple(zip(train_data['text'].tolist(), train_data['information_about'].tolist()))
    print(data[1])
    docs = []

    nlp = spacy.load("hu_core_news_lg")
    for doc, label in tqdm(nlp.pipe(data, as_tuples=True), total=len(data)):

        if label == 'information':
            doc.cats['information'] = 1
            doc.cats['order'] = 0
            doc.cats['order_modification'] = 0
            doc.cats['complaint'] = 0
            doc.cats['search'] = 0
        elif label == 'order':
            doc.cats['information'] = 0
            doc.cats['order'] = 1
            doc.cats['order_modification'] = 0
            doc.cats['complaint'] = 0
            doc.cats['search'] = 0
        elif label == 'order_modification':
            doc.cats['information'] = 0
            doc.cats['order'] = 0
            doc.cats['order_modification'] = 1
            doc.cats['complaint'] = 0
            doc.cats['search'] = 0
        elif label == 'complaint':
            doc.cats['information'] = 0
            doc.cats['order'] = 0
            doc.cats['order_modification'] = 0
            doc.cats['complaint'] = 1
            doc.cats['search'] = 0
        elif label == 'search':
            doc.cats['information'] = 0
            doc.cats['order'] = 0
            doc.cats['order_modification'] = 0
            doc.cats['complaint'] = 0
            doc.cats['search'] = 1

        docs.append(doc)

    return docs, train_data


train_docs, train_data = make_docs(type="train")
doc_bin = DocBin(docs=train_docs)
doc_bin.to_disk("./textcat_data/textcat_train.spacy")

test_docs, test_data = make_docs(type="valid")
doc_bin = DocBin(docs=test_docs)
doc_bin.to_disk("./textcat_data/textcat_valid.spacy")
