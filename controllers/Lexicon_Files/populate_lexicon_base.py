import pandas as pd
import os

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files")

posiFile = pd.read_csv(file_path + "/positive.txt", header=None)
posi_list = posiFile[0].tolist()

nega_file = pd.read_csv(file_path + "/negative.txt", header=None)
nega_list = nega_file[0].tolist()

afinn = pd.read_csv(file_path + "/afinn.csv")
afinn_positive = afinn[afinn['score'] > 0]['word'].tolist()
afinn_negative = afinn[afinn['score'] < 0]['word'].tolist()

fil_words = pd.read_excel(file_path + "/fil_words_senti.xlsx")
fil_positive_list = fil_words[fil_words['positivity'] > fil_words['negativity']]['word'].tolist()
fil_negative_list = fil_words[fil_words['positivity'] < fil_words['negativity']]['word'].tolist()

fil_positive_list_final = []
for word in fil_positive_list:
    word = word.lower()
    word = word.replace("-", " ")
    word = word.replace("_", " ")
    if ',' in word:
        fil_positive_list_final.extend(word.split(','))
    else:
        fil_positive_list_final.append(word)

fil_negative_list_final = []
for word in fil_negative_list:
    word = word.lower()
    word = word.replace("-", " ")
    word = word.replace("_", " ")
    if ',' in word:
        fil_negative_list_final.extend(word.split(','))
    else:
        fil_negative_list_final.append(word)

posi_list.extend(afinn_positive)
nega_list.extend(afinn_negative)

posi_list_final = list(set(posi_list))
nega_list_final = list(set(nega_list))

file_path = os.path.join(file_path, "final_sentiment_words")

# save word list per sentiment in a file
df = pd.DataFrame(posi_list_final, columns=["word"])
df.to_csv(file_path+'/positive_sentiment_words_english.csv', index=False)

df = pd.DataFrame(nega_list_final, columns=["word"])
df.to_csv(file_path+'/negative_sentiment_words_english.csv', index=False)

df = pd.DataFrame(fil_positive_list_final, columns=["word"])
df.to_csv(file_path+'/positive_sentiment_words_filipino.csv', index=False)

df = pd.DataFrame(fil_negative_list_final, columns=["word"])
df.to_csv(file_path+'/negative_sentiment_words_filipino.csv', index=False)


