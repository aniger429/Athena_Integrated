import unicodedata as uni

# as of unicodedata version 8.0.0

def pos_file_to_list():
    posiFile = pd.read_csv("C:/Users/HKJ/AppData/Local/Programs/Python/Python35/positive.txt", header=None)
    posi_list = posiFile[0].tolist()
    return posi_list

def neg_file_to_list():
    nega_file = pd.read_csv("C:/Users/HKJ/AppData/Local/Programs/Python/Python35/negative.txt", header=None)
    nega_list = nega_file[0].tolist()
    return nega_list

def pos(string, posi_list):
    for i in range(0, len(posi_list)):
        if uni.lookup(posi_list[i]) in string:
            string = string.replace(uni.lookup(posi_list[i]), ' POSITIVE_EMOTICON ')
    return string

def neg(string, nega_list):
    for i in range(0, len(nega_list)):
        if uni.lookup(nega_list[i]) in string:
            string = string.replace(uni.lookup(nega_list[i]), ' NEGATIVE_EMOTICON ')
    return string
            
