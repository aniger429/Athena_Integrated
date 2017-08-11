from DBModels.Lexicon import *

posEng = get_all_words("english", "positive")
negEng = get_all_words("english", "negative")
posFil = get_all_words("filipino", "positive")
negFil = get_all_words("filipino", "negative")


def tweet_words_positive(tweet):
    array = []
    splitter = tweet.split()
    for word in splitter:
        if (word in posEng) or (word in posFil):
            print(word + ': Positive')
            array.append(word)
    return array


def tweet_words_negative(tweet):
    array = []
    splitter = tweet.split()
    for word in splitter:
        if (word in negEng) or (word in negFil):
            print(word + ': Negative')
            array.append(word)
    return array   


def get_sentiment(tweet):
    word_list = []
    for word in tweet.split(' '):
        if (word in negEng) or (word in negFil):
            print(word + ': negative')
            word_list.append((word, 'negative'))
        elif (word in posEng) or (word in posFil):
                print(word + ': positive')
                word_list.append((word, 'positive'))
        else:
            word_list.append((word, 'neutral'))

    return word_list
a = get_sentiment('i am not happy')
print(a)

