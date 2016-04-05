from collection.collect_positive import create_json
from collection.gen_csv import gen_csv as gen_csv_ny
from utils.common import remove_non_ascii as rm_ascii
from utils.output import convert_json
from collection.collect import clean, fetch_url, write_to_folder
import json

# NLP Module Init#
SPACY_FLAG = True # Use Spacy if set as true
KEYWORD = "keyword.json"
KEYWORD_FILE = "keyword_in_file.json"


# Spacy Module
if SPACY_FLAG is True:
    from spacy.en import English
    from nlp.spacy_nlp import nlp_get_words as spacy_get_words
    parser = English()
    sent_detector, tagger, pstemmer = None, None, None
else:
    parser = None
    # NLTK Module
    import nltk.data
    from nltk.stem.porter import *
    from nltk.tag.perceptron import PerceptronTagger
    from nlp.nltk_nlp import nlp_get_words as nltk_get_words
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    tagger = PerceptronTagger()
    pstemmer = PorterStemmer()



def read_urls(file):
    with open(file) as data:
        fin = json.load(data)
        dic = {}
        key_in_file = {}
        for file_entry in fin:
            url = fin[file_entry]["url"]
            if "nytimes" in url:
                handle_ny_times(url)
                break
            else:
                filename, result_dic = handle_others(url, file_entry)
                dic.update(result_dic)
                key_in_file[filename] = {}
                key_in_file[filename]["type"] = fin[file_entry]["type"]
                key_in_file[filename]["keywords"] = result_dic[filename]
        if len(dic) > 0:
            keyword_json = open(KEYWORD, 'w+')
            file_json = open(KEYWORD_FILE, 'w+')
            try:
                dat = json.load(keyword_json)
                filename = json.load(file_json)
            except ValueError, e:
                print "Empty file or wrong json format", e.message
                dat = {}
                filename = {}
            # print dat
            for key in dic:
                keyword_dic = dic[key]
                for k in keyword_dic:
                    if k in dat:
                        dat[k]["total"] += keyword_dic[k]
                        dat[k]["value"].append(keyword_dic[k])
                        dat[k]["files"].append(key)
                    else:
                        dat[k] = {}
                        dat[k]["total"] = keyword_dic[k]
                        dat[k]["value"] = [keyword_dic[k]]
                        dat[k]["files"] = [key]
            filename.update(key_in_file)
            json.dump(dat, keyword_json, indent=2,sort_keys=True)
            json.dump(filename, file_json, indent=2, sort_keys=True)
            keyword_json.close()
            file_json.close()
            convert_json(KEYWORD, KEYWORD_FILE)
        else:
            print "No new file added"
    


def handle_ny_times(url):
    prefix = "new-ny"
    create_json(url, None)
    gen_csv_ny('../../dat/NYnegative/json', '../../dat/NYpositive/json', '../../dat/undecided/json')
    print "Use Weka to classify and then move the file to the right folder"


def handle_others(url, filename):
    dic = {}
    html = fetch_url(url)
    if html != -1:
        final, remove_tag = clean(html)
        import time
        final = rm_ascii(final)
        write_to_folder("../dat/new", filename, final)
        if SPACY_FLAG is True:
            print "using spacy"
            words = spacy_get_words(parser, final)
        else:
            print "using nltk"
            words = nltk_get_words(final, sent_detector, pstemmer, tagger)
        dic[filename] = words
    return filename, dic

if __name__ == "__main__":
    read_urls("file.json")
