from __future__ import print_function

from _csv import writer
from random import random, sample, randrange

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '18wznOXgXRYAED9QBpG0-HSdRI8krz-yRYuNBrp2rhHw'


def append_row(type, values):
    range = get_range(type)
    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        request = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                      range=range,
                                      valueInputOption="USER_ENTERED",
                                      insertDataOption="INSERT_ROWS",
                                      body={"values": values}).execute()

    except HttpError as err:
        print(err)


def get_ner_sentences(type):
    spreadsheet_range = get_range(type)
    ner_sentences = []

    try:
        service = build('sheets', 'v4', credentials=credentials)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=spreadsheet_range).execute()
        values = result.get('values', [])
        for row in values:
            ner_sentences.append(row)
    except HttpError as err:
        print(err)

    return ner_sentences


def create_textcat_sentences(type):
    spreadsheet_range = get_range(type)
    file_name = ""
    try:
        service = build('sheets', 'v4', credentials=credentials)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=spreadsheet_range).execute()
        values = result.get('values', [])

        file_name = "train_weight.csv" if type == "text_classifier_training" else "valid_weight.csv"

        not_really_randomised_list = []
        counter = 0
        for row in values:
            counter += int(row[3])
            for x in range(0, int(row[3])):
                not_really_randomised_list.insert(randrange(0, len(not_really_randomised_list) + 1), [row[0], row[1], row[2]])
        really_randomised_list = [0 for x in range(counter)]
        random_numbers_with_no_duplicates = sample(range(counter), counter)

        for elem in not_really_randomised_list:
            for random_number in random_numbers_with_no_duplicates:
                really_randomised_list[random_number] = elem
                random_numbers_with_no_duplicates.remove(random_number)
                break

        with open(file_name, 'w', encoding='utf-8', newline='') as writer_obj:
            csv_writer = writer(writer_obj)
            csv_writer.writerow(["textID", "text", "information_about"])

            for really_random_sentence in not_really_randomised_list:
                csv_writer.writerow(really_random_sentence)

    except HttpError as err:
        print(err)
    return file_name


def get_range(type):
    switcher = {
        "text_classifier_training": "text_classifier_training",
        "text_classifier_valid": "text_classifier_valid",
        "ner_training": "ner_training",
        "ner_valid": "ner_valid"
    }
    return switcher.get(type)
