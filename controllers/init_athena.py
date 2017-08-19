import os

import pandas as pd

from DBModels.Lexicon import insert_lexicon_sentiments


# init lexicon database
def populate_lexicon():
    script_path = os.path.dirname(os.path.dirname(__file__))
    file_path_lexicons = os.path.join(script_path, "controllers", "Lexicon_Files", "final_sentiment_words")

    e_positive_list = pd.read_csv(file_path_lexicons+"/positive_sentiment_words_english.csv", squeeze=True).tolist()
    f_positive_list = pd.read_csv(file_path_lexicons + "/positive_sentiment_words_filipino.csv", squeeze=True).tolist()
    e_negative_list = pd.read_csv(file_path_lexicons + "/negative_sentiment_words_english.csv", squeeze=True).tolist()
    f_negative_list = pd.read_csv(file_path_lexicons + "/negative_sentiment_words_filipino.csv", squeeze=True).tolist()

    insert_lexicon_sentiments("english", e_positive_list, e_negative_list)
    insert_lexicon_sentiments("filipino", f_positive_list, f_negative_list)
