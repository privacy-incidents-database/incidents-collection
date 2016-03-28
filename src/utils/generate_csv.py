import json
import math
import csv

KEYWORD = "../keyword.json"
KEYWORD_FILE = "../keyword_in_file.json"
RESULT = "../result.csv"


'''
keyword.json
{
    "abc":{
        "total": 4,
        "value":[1,3],
        "file": [file1,file2],
    }
}

keyword_in_file.json
{
    "file1" : [word1, word2],
    "file2" : [word2, word3]
}


'''


def convert_json():
    fin = open(KEYWORD)
    fin2 = open(KEYWORD_FILE)
    dat = json.load(fin)
    filename = json.load(fin2)
    fout = open(RESULT)
    out = csv.writer(fout)
    tfidf_log = {}
    title = ['filename', 'isPrivacy']
    keyword_list = []
    for key in dat:
        tfidf_log[key] = float(math.log10(len(dat.keys()/dat[key]["total"])))
        title.append(key)
        keyword_list.append(key)
    out.writerow(title.extend(keyword_list))
    for key in filename:
        val = [0] * (len(keyword_list))
        for word in filename[key]:
            idx = keyword_list.index(word)
            file_idx = dat[word]["file"].index(key)
            val[idx] = float(dat[word]["value"][file_idx]*tfidf_log[word])
        result = [key, 'TBD']
        result.extend(val)
        out.writerow(result)




