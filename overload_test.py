import keyword_extractor
import ner
import spreadsheet_handler
import textcat


def runallsentence():
    sentences = spreadsheet_handler.get_all_sentences("text_classifier_training")

    for sentence in sentences:
        params = keyword_extractor.get_hotwords(sentence)

        paramNames = ner.getner(sentence)

        data = [sentence, textcat.getcat(sentence)['intent']['intent_name'],
                textcat.getcat(sentence)['intent']['intent_percentage'],
                paramNames, params, textcat.getcat(sentence)['other_intent']]

        print(data)
