from collection.collect_positive import create_json
from collection.gen_csv import gen_csv as gen_csv_ny
from nlp.spacy_nlp import nlp_get_words as spacy_get_words
from nlp.nltk_nlp import nlp_get_words as nltk_get_words
from utils.common import remove_non_ascii as rm_ascii
from collection.collect import clean, fetch_url, write_to_folder
from nlp.tfidf_log import gen_csv as tfidf_log
import json




# NLP Module Init#
SPACY_FLAG = True # Use Spacy if set as true

# Spacy Module
if SPACY_FLAG is True:
    from spacy.en import English
    parser = English()
    sent_detector, tagger, pstemmer = None, None, None

else:
    parser = None
    # NLTK Module
    import nltk.data
    from nltk.stem.porter import *
    from nltk.tag.perceptron import PerceptronTagger
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    tagger = PerceptronTagger()
    pstemmer = PorterStemmer()

KEYWORD = "keyword.json"
KEYWORD_FILE = "keyword_in_file.json"

def read_urls(file):
    with open(file) as data:
        dic = {}
        key_in_file = {}
        for url in data.readline():
            if "nytimes" in url:
                handle_ny_times(url)
                break
            else:
                filename, result_dic = handle_others(url)
                dic.update(result_dic)
                key_in_file[filename] = result_dic.keys()
        if len(dic) > 0:
            keyword_json = open(KEYWORD, 'rw')
            file_json = open(KEYWORD_FILE, 'rw')
            dat = json.load(keyword_json)
            filename = json.load(file_json)
            for key in dic:
                keyword_dic = dic[key]
                for k in keyword_dic:
                    if k in dat:
                        dat[k]["total"] += keyword_dic[k]
                        dat[k]["value"].append(keyword_dic[k])
                        dat[k]["file"].append(key)
            filename.update(key_in_file)
            json.dump(dat, KEYWORD, indent=2)
            json.dump(filename, KEYWORD_FILE, indent=2)
        else:
            print "No new file added"


def handle_ny_times(url):
    prefix = "new-ny"
    create_json(url, None)
    gen_csv_ny('../../dat/NYnegative/json', '../../dat/NYpositive/json', '../../dat/undecided/json')
    print "Use Weka to classify and then move the file to the right folder"


def handle_others(url):
    dic = {}
    html = fetch_url(url)
    if html != -1:
        final, remove_tag = clean(html)
        import time
        final = rm_ascii(final)
        filename = str(time.time())
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
    print "here"
    read_urls("file")

