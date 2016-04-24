import json
import math
import csv
import sys

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


def convert_json(keyword, keyword_file):
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
    keyword_map = {}
    count = 0
    for key in dat:
        key_len = len(dat.keys())
        tfidf_log[key] = float(math.log10(key_len/dat[key]["total"]))
        title.append(key)
        keyword_map[key] = count
        count+=1
    out_test.writerow(title)
    out_training.writerow(title)

    file_cnt = 0
    total_articles = len(filename_file)

    for entry in filename_file:
        file_cnt += 1
        sys.stdout.write("\rGenerating tfidf csv : " + str(
            int((float(file_cnt) / float(total_articles)) * 100)) + "% Complete")

        val = [0] * (len(keyword_map))
        # Recalculate the value using the actual appearance in the article times tfidf value of the word
        for word in filename_file[entry]["keywords"]:
            idx = keyword_map[word]
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


# if __name__ == "__main__":
#     convert_json("../keyword.json", "../keyword_in_file.json")
