from DBModels.KB_Names import *
from DBModels.Tweet import *


def find_more_names():
    unigram_list = get_all_unigrams()
    candidate_names = get_all_kb_names()
    results = {}
    # print(unigram_list)

    for candidate in candidate_names:
        results[candidate['candidate_name']] = list(set([str for str in unigram_list
                                                         if any(name in str for name in candidate['kb_names'])
                                                         and (str not in candidate['blacklist_names'])]))

    # print(results)
    kb_names_update(results)
