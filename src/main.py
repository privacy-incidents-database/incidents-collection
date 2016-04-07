from collection.collect_positive import create_json
from collection.gen_csv import gen_csv as gen_csv_ny
from utils.common import remove_non_ascii as rm_ascii
from utils.output import convert_json
from collection.collect import clean, fetch_url, write_to_folder
import json
import os.path

# NLP Module Init#
SPACY_FLAG = False  # Use Spacy if set as true
KEYWORD = "keyword.json"
KEYWORD_FILE = "keyword_in_file.json"


# Spacy Module
if SPACY_FLAG is True:
    print "using spacy"
    from spacy.en import English
    from nlp.spacy_nlp import nlp_get_words as spacy_get_words
    parser = English()
    sent_detector, tagger, pstemmer = None, None, None
else:
    print "using nltk"
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
    with open(file) as input_data:
        input_json = json.load(input_data)
        new_keyword_dic = {}
        new_file_dic = {}
        mode = 'r' if os.path.exists(KEYWORD) else 'w'
        with open(KEYWORD, mode) as old_keyword_f:
            try:
                old_keyword_dic = json.load(old_keyword_f)
            except Exception, e:
                print "Empty file or wrong json format for keyword dic", e.message
                old_keyword_dic = {}
        with open(KEYWORD_FILE, mode) as old_filename_f:
            try:
                old_file_dic = json.load(old_filename_f)
            except Exception, e:
                print "Empty file or wrong json format for file dic", e.message
                old_file_dic = {}
        for file_entry in input_json:
            if file_entry in old_file_dic:
                print "this file is already in json."
                continue
            url = input_json[file_entry]["url"]
            if "nytimes" in url:
                handle_ny_times(url)
                break
            else:
                name, result_dic = handle_others(url, file_entry)
                new_keyword_dic.update(result_dic)
                new_file_dic[name] = {}
                new_file_dic[name]["type"] = input_json[file_entry]["type"]
                new_file_dic[name]["keywords"] = result_dic[name]
        if len(new_keyword_dic) > 0:
            for key in new_keyword_dic:
                keyword_dic = new_keyword_dic[key]
                for k in keyword_dic:
                    if k in old_keyword_dic:
                        old_keyword_dic[k]["total"] += keyword_dic[k]
                        old_keyword_dic[k]["value"].append(keyword_dic[k])
                        old_keyword_dic[k]["files"].append(key)
                    else:
                        old_keyword_dic[k] = {}
                        old_keyword_dic[k]["total"] = keyword_dic[k]
                        old_keyword_dic[k]["value"] = [keyword_dic[k]]
                        old_keyword_dic[k]["files"] = [key]
            old_file_dic.update(new_file_dic)
            with open(KEYWORD, 'w') as new_keyword_f:
                try:
                    json.dump(old_keyword_dic, new_keyword_f, indent=2, sort_keys=True)
                except Exception, e:
                    print "Error writing to file for keyword dic", e.message
            with open(KEYWORD_FILE, 'w') as new_filename_f:
                try:
                    json.dump(old_file_dic, new_filename_f, indent=2, sort_keys=True)
                except Exception, e:
                    print "Error writing to file for filename dic", e.message
            convert_json(KEYWORD, KEYWORD_FILE)
            print "Finished"
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
        final = rm_ascii(final)
        write_to_folder("../dat/new", filename, final)
        if SPACY_FLAG is True:

            words = spacy_get_words(parser, final)
        else:

            words = nltk_get_words(final, sent_detector, pstemmer, tagger)
        dic[filename] = words
    return filename, dic

if __name__ == "__main__":
    import os
    read_urls(os.sys.argv[1])
