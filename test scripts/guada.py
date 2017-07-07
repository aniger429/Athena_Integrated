# from multiprocessing import Pool
# import numpy as np
#
# num_partitions = 6  # number of partitions to split dataframe
# num_cores = 6  # number of cores on your machine
#
# def write_csv(df):
#     df.to_csv("/home/dudegrim/Documents/Testing/guada_tweets2.csv", sep=',',
#                 columns=['orig_tweets', 'tweet', 'binay', 'duterte', 'poe', 'roxas', 'santiago', 'sentiment'], index=None)
#
#     return
#
# def parallelize_dataframe(df, func):
#     df_split = np.array_split(df, num_partitions)
#     pool = Pool(num_cores)
#     df = pd.concat(pool.map(func, df_split))
#     pool.close()
#     pool.join()
#     return df
#
#
# def multiply_columns(tweets):
#     print("done 1")
#     tweets['sentiment'] = tweets.apply(lambda row: test_senti_ana(row['tweet']), axis=1)
#     return tweets
#
#
# def senti():
#
#     tweets = read_csv("/home/dudegrim/Documents/Testing/guada_tweets1.csv")
#
#     print("start")
#     start = time.time()
#     results = parallelize_dataframe(tweets, multiply_columns)
#     end = time.time()
#
#     print(end - start)
#     print("sentiment analysis done")
#
#     write_csv(results)
#
#
# def candi():
#     tweets = get_all_orig_tweets()
#
#     results = test_identify_candidate(tweets)
#     print("candidate analysis done")
#
#     df1 = pandas.DataFrame(results)
#
#     print(len(df1.index))
#
#     write_csv(df1)
#
#
# def check_data():
#     df = read_csv("/home/dudegrim/Documents/Testing/guada_tweets1.csv")
#     # final = df[(df['duterte'] == 1)].head(n=10000)
#     # final.append(df[(df['roxas'] == 1)].head(n=10000), ignore_index=False)
#     # final.append(df[(df['binay'] == 1)].head(n=10000), ignore_index=False)
#     # final.append(df[(df['santiago'] == 1)].head(n=10000), ignore_index=False)
#     # final.append(df[(df['poe'] == 1)].head(n=10000), ignore_index=False)
#
#     final = df.drop(df[(df.duterte == 1) & (df.binay == 0) & (df.santiago == 0) & (df.roxas == 0) & (df.poe == 0)].index)
#
#     print(len(final[(final['binay'] == 1)]))
#     print(len(final[(final['duterte'] == 1)]))
#     print(len(final[(final['santiago'] == 1)]))
#     print(len(final[(final['roxas'] == 1)]))
#     print(len(final[(final['poe'] == 1)]))
#
#     write_csv(final)