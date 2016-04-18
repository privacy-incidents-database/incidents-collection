from collection.collect_positive import create_json
from collection.gen_csv import gen_csv as gen_csv_ny
from utils.common import remove_non_ascii as rm_ascii
from utils.output import convert_json
from collection.collect import clean, fetch_url, write_to_folder
import json
import os.path

# NLP Module Init#
SPACY_FLAG = False  # Use Spacy if set as true

#File used to store the previous keywords
KEYWORD = "keyword.json"
#File used to store the existing news/file/url
KEYWORD_FILE = "keyword_in_file.json"

# Load only when necessary
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




# Read urls from input file
# Accept file input as

'''
{
  "hashed_url": {
    "url": "http://www.wired.com/2012/02/google-safari-browser-cookie/",
    "type": 0
  },
  "ac578aabe6a13294d98d5862562956e4aa1c8ece": {
    "url": "http://www.latimes.com/business/la-fi-mugshots-lawsuit-20140121-story.html#axzz2sCXHQMCZ",
    "type": 0
  }
}



'''
#Type is defined through
'''
Privacy Incidents - 0
Computer Security - 1
General Security - 2
Random Articles - 3
Privacy Articles but not incidents - 4
Test Articles - TBD
'''

def read_urls(file):
    with open(file) as input_data:
        input_json = json.load(input_data)
        # new_key_word_dic is used to store the keywords generated this time only
        new_keyword_dic = {}
        # new_file_dic is used to store the filename this time only
        new_file_dic = {}
        # create files if not exist
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
            # Continue when the url(hashed) already exists
            if file_entry in old_file_dic:
                print "this file is already in json."
                continue

            url = input_json[file_entry]["url"]

            ## Approach 1 (Currently Unused)
            ## for nytimes need to handle that using the json field instead of text mining to get more accurate result
            if "nytimeeees" in url:
                handle_ny_times(url)
                break

            ## Approach 2 use text mining (Currently used)
            else:
                name, result_dic = handle_others(url, file_entry)
                if len(result_dic) == 0:
                    continue
                new_keyword_dic.update(result_dic)
                new_file_dic[name] = {}
                new_file_dic[name]["type"] = input_json[file_entry]["type"]
                new_file_dic[name]["keywords"] = result_dic[name]

        # If new data has been added through this file, will update the keywords and file_entry file to store this result.
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
            # generate the csv for weka.
            convert_json(KEYWORD, KEYWORD_FILE)
            print "Finished"
        else:
            print "No new file added"

# Call the functions to generate the attribute which can be got from NYtimes Api
def handle_ny_times(url):
    prefix = "new-ny"
    create_json(url, None)
    gen_csv_ny('../../dat/NYnegative/json', '../../dat/NYpositive/json', '../../dat/undecided/json')
    print "Use Weka to classify and then move the file to the right folder"

# Call text mining(NLP) module to get the keywords dic and filename
def handle_others(url, filename):
    dic = {}
    html = fetch_url(url)
    if html != -1:
        final, remove_tag = clean(html)
        final = rm_ascii(final)
        write_to_folder("../dat/new", filename, final)
        # Use different tool to get the nlp result...
        # All modification deals with nlp should be done in the nlp module.
        if SPACY_FLAG is True:
            words = spacy_get_words(parser, final)
        else:
            words = nltk_get_words(final, sent_detector, pstemmer, tagger)
        dic[filename] = words
    return filename, dic

if __name__ == "__main__":
    import os
    read_urls(os.sys.argv[1])
