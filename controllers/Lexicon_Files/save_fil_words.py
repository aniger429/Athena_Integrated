import pandas as pd
import os

script_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(script_path, "Lexicon_Files")


def get_word_list():
    filDict = []
    wordList = dict()

    filDictFile = open(file_path + "/final.txt", 'r', encoding="utf-8")
    filDictCount = len(filDictFile.readlines())
    filDictFile.close()

    filDictFile = open(file_path + "/final.txt", 'r', encoding="utf-8")
    for i in range(0, filDictCount):
        filDict.append(filDictFile.readline())

    filStopFile = open(file_path + "/fil-words.txt", 'r')
    filStopCount = len(filStopFile.readlines())
    filStopFile.close()

    filStopFile = open(file_path + "/fil-words.txt", 'r')
    filsw = dict()
    filscorelist = []
    for i in range(0, filStopCount):
        filsw.update({filStopFile.readline() : 'blank'})

    for i in range(0, filDictCount):
        line = filDict[i]
        if "<positivity>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filscorelist.append(float(line[0 : line.index("<")]))
        if "<negativity>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filscorelist.append(float(line[0 : line.index("<")]))
        if "<translation>" in line:
            line = line[(line.index(">") + 1) : len(line)]
            filword = line[0 : line.index("<")]
            if not filword in filsw:
                if len(filscorelist) > 0:
                    wordList.update({filword : filscorelist})
            filword = ""
            filscorelist = []
            line = filDict[i+1]
            while "<translation>" in line:
                i = i + 1
                line = filDict[i]

    filscorelist = []
    for i in range(0, filDictCount):
        line = filDict[i]
        if "<positivity>" in line:
            line = line[(line.index(">") + 1): len(line)]
            filscorelist.append(float(line[0: line.index("<")]))
        if "<negativity>" in line:
            line = line[(line.index(">") + 1): len(line)]
            filscorelist.append(float(line[0: line.index("<")]))
        if "<translation>" in line:
            for j in range(0, 2):
                i = i + 1
                line = filDict[i]
                if "<translation>" in line:
                    line = line[(line.index(">") + 1): len(line)]
                    filword = line[0: line.index("<")]
                    if not filword in wordList:
                        if len(filscorelist) > 0:
                            wordList.update({filword: filscorelist})
                else:
                    break
            line = filDict[i+1]
            while "<translation>" in line:
                i = i + 1
                line = filDict[i]
            filscorelist = []

    return wordList


def save_list(wordList):
    list_of_words = []
    for key, value in wordList.items():
        list_of_words.append({'word': key, 'positivity': value[0], 'negativity': value[1]})

    data = pd.DataFrame(list_of_words)
    data.set_index("word", drop=True, inplace=True)
    data.to_excel("fil_words_senti.xlsx", index='word')


# wordList = get_word_list()
# save_list(wordList)


fil_words = pd.read_excel(file_path + "/fil_words_senti.xlsx", index_col='word')
fil_dict = fil_words[:10].to_dict(orient='index')
start = time.time()
val = fil_dict.get('banana', {}).get('negativity',0)
end = time.time()
print(end-start)


# 'tagapamagitan': {'negativity': 0.25, 'positivity': 0.0}