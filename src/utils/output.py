import json
import math
import csv

KEYWORD = "../keyword.json"
KEYWORD_FILE = "../keyword_in_file.json"
TEST = "test.csv"
TRAINING = "training.csv"

'''
keyword.json
{
    "abc":{
        "total": 4,
        "value":[1,3],
        "files": [file1,file2],
    }
}

keyword_in_file.json
{
    "file1" : [word1, word2],
    "file2" : [word2, word3]
}


'''


def convert_json(keyword=KEYWORD, keyword_file=KEYWORD_FILE):
    fin = open(keyword, 'r')
    fin2 = open(keyword_file, 'r')
    dat = json.load(fin)
    filename_file = json.load(fin2)
    test_file = open(TEST, 'w+')
    training_file = open(TRAINING, 'w+')
    out_test = csv.writer(test_file)
    out_training = csv.writer(training_file)
    tfidf_log = {}
    title = ['filename', 'isPrivacy']
    keyword_list = []
    for key in dat:
        key_len = len(dat.keys())
        tfidf_log[key] = float(math.log10(key_len/dat[key]["total"]))
        title.append(key)
        keyword_list.append(key)
    title.extend(keyword_list)
    out_test.writerow(title)
    out_training.writerow(title)
    for entry in filename_file:
        val = [0] * (len(keyword_list))
        for word in filename_file[entry]["keywords"]:
            idx = keyword_list.index(word)
            file_idx = dat[word]["files"].index(entry)
            val[idx] = float(dat[word]["value"][file_idx]*tfidf_log[word])
        if filename_file[entry]["type"] == "TBD":
            test = [entry, 'TBD']
            test.extend(val)
            out_test.writerow(test)
        else:
            training = [entry, filename_file[entry]["type"]]
            training.extend(val)
            out_training.writerow(training)
    test_file.close()
    training_file.close()
# convert_json()


