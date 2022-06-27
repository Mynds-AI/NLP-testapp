import spacy
import pandas as pd
import re
import string

from tqdm.auto import tqdm
from spacy.tokens import DocBin


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


def remove_url(text):
    url_pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return url_pattern.sub(r'', text)


def clean_text(text):
    delete_dict = {sp_character: '' for sp_character in string.punctuation}
    delete_dict[' '] = ' '
    table = str.maketrans(delete_dict)
    text1 = text.translate(table)
    # print('cleaned:'+text1)
    textArr = text1.split()
    text2 = ' '.join([w for w in textArr if (not w.isdigit() and (not w.isdigit() and len(w) > 3))])

    return text2.lower()


def make_docs(file_path):
    """
    this will take a list of texts and labels
    and transform them in spacy documents

    data: list(tuple(text, label))

    returns: List(spacy.Doc.doc)
    """
    train_data = pd.read_csv(file_path)
    train_data.dropna(axis=0, how='any', inplace=True)
    train_data['Num_words_text'] = train_data['text'].apply(lambda x: len(str(x).split()))
    mask = train_data['Num_words_text'] > 2
    train_data = train_data[mask]
    print(train_data['information_about'].value_counts())

    train_data['text'] = train_data['text'].apply(remove_emoji)
    train_data['text'] = train_data['text'].apply(remove_url)
    train_data['text'] = train_data['text'].apply(clean_text)

    data = tuple(zip(train_data['text'].tolist(), train_data['information_about'].tolist()))
    print(data[1])
    docs = []
    # nlp.pipe([texts]) is way faster than running
    # nlp(text) for each text
    # as_tuples allows us to pass in a tuple,
    # the first one is treated as text
    # the second one will get returned as it is.
    nlp = spacy.load("hu_core_news_lg")
    for doc, label in tqdm(nlp.pipe(data, as_tuples=True), total=len(data)):

        # we need to set the (text)cat(egory) for each document
        # print(label)
        if label == 'information':
            doc.cats['information'] = 1
            doc.cats['order'] = 0
            doc.cats['order_modification'] = 0
            doc.cats['complaint'] = 0
        elif label == 'order':
            doc.cats['information'] = 0
            doc.cats['order'] = 1
            doc.cats['order_modification'] = 0
            doc.cats['complaint'] = 0
        elif label == 'order_modification':
            doc.cats['information'] = 0
            doc.cats['order'] = 0
            doc.cats['order_modification'] = 1
            doc.cats['complaint'] = 0
        elif label == 'complaint':
            doc.cats['information'] = 0
            doc.cats['order'] = 0
            doc.cats['order_modification'] = 0
            doc.cats['complaint'] = 1

        docs.append(doc)

    return docs, train_data


train_docs, train_data = make_docs("./train.csv")
# then we save it in a binary file to disc
doc_bin = DocBin(docs=train_docs)
doc_bin.to_disk("./textcat_data/textcat_train.spacy")

test_docs, test_data = make_docs("./test.csv")
#then we save it in a binary file to disc
doc_bin = DocBin(docs=test_docs)
doc_bin.to_disk("./textcat_data/textcat_valid.spacy")