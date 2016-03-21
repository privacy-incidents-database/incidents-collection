from collection.collect_positive import create_json
from collection.gen_csv import gen_csv
from nlp.spacy_nlp import nlp
from utils.common import remove_non_ascii as rm_ascii
from collection.collect import clean, fetch_url, write_to_folder
from nlp.tfidf_log import gen_csv as tfidf_log
import json


new_key = {}
KEYWORD = "keyword.json"
def read_urls(file):
    with open(file) as data:
        for url in data.readline():
            if "nytimes" in url:
                handle_ny_times(url)
                break
            else:
                handle_others(url)
        if len(new_key)>0:
            fin = open(KEYWORD)
            dat = json.load(fin)
            for key in new_key:
                if key in dat:
                    dat[key] += new_key[key]
                else:
                    dat[key] = new_key[key]
            tfidf_log("","",dat)





def handle_ny_times(url):
    prefix = "new-ny"
    create_json(url, None)
    gen_csv('../../dat/NYnegative/json', '../../dat/NYpositive/json', '../../dat/undecided/json')
    print "Use Weka to classify and then move the file to the right folder"


def handle_others(url):
    html = fetch_url(url)
    if html != -1:
        final, remove_tag = clean(html)
        import time
        write_to_folder("../dat/new",str(time.time()),remove_tag,final)
        filtered = rm_ascii(final)
        words = {}
        nouns, adj, adv, verbs = nlp(text)
        words= nouns.copy()
        words.update(adj)
        words.update(adv)
        words.update(verbs)
        for key in words:
            if key in new_key:
                new_key[key] += 1
            else:
                new_key[key] = 1
        json.dump(words)




def __handle__(text):





