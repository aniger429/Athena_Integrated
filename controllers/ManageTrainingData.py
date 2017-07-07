import pandas as pd

columns = ['Tweet', 'Sentiment']


def writeToFile(data, filename):
    d = pd.DataFrame.from_dict(data)
    df = pd.DataFrame(data=d, index=None)
    df.to_excel(filename, index=False)


def read_csv(filename):
    return pd.read_csv(filename, encoding="utf8", keep_default_na=False, index_col=None, sep=",",
                       skipinitialspace=True, chunksize=10000, usecols=columns)


def write_csv(filename, tweets):
    import os
    # if file does not exist write header
    if not os.path.isfile(filename):
        return tweets.to_csv(filename, header=True, sep=',', index=False, columns=columns, chunksize=10000)
    else:  # else it exists so append without writing the header
        return tweets.to_csv(filename, mode='a', sep=',', index=False, header=False, columns=columns, chunksize=10000)


def write_data(filename, data):
    import os
    # if file does not exist write header
    if not os.path.isfile(filename):
        return data.to_csv(filename, header=True, sep=',', index=False)
    else:  # else it exists so append without writing the header
        return data.to_csv(filename, mode='a', sep=',', index=False, header=False)


def test(filename):
    print("start")
    reader = read_csv(filename)
    data = pd.DataFrame()

    for chunk in reader:
        data = data.append(chunk, ignore_index=True)

    positive_tweets = data.loc[data['Sentiment'] == "Positive"]
    neutral_tweets = data.loc[data['Sentiment'] == "Neutral"]
    negative_tweets = data.loc[data['Sentiment'] == "Negative"]

    print("saving")

    write_csv("/home/dudegrim/Documents/Training/positive_tweets.csv", positive_tweets)
    write_csv("/home/dudegrim/Documents/Training/neutral_tweets.csv", neutral_tweets)

    print("almost")
    write_csv("/home/dudegrim/Documents/Training/negative_tweets.csv", negative_tweets)

    data_count = pd.DataFrame({'Positive': len(positive_tweets), 'Neutral': len(neutral_tweets),
                               'Negative': len(negative_tweets)}, index=[0])

    write_data("/home/dudegrim/Documents/Training/data_count.csv", data_count)

    print("done")

# 0-3 done
for r in range(0,10,1):
    print(r)
    directory = "/home/dudegrim/Documents/CSV8/Election-"+str(r)+".csv"
    test(directory)
