#-*- coding: utf-8 -*-

import os
import json
import argparse
import nltk.data
from nltk.stem.porter import *
from nltk.tag.perceptron import PerceptronTagger


def get_args():
    global args
    parser = argparse.ArgumentParser(
        description="Script for performing NLP using nltk")
    parser.add_argument(
        "directory", help='Name of the directory containing Articles')
    args = parser.parse_args()
    return args

# args = get_args()


def traverse(sent_detector, src):
    tagger = PerceptronTagger()
    pstemmer = PorterStemmer()

    for filename in os.listdir(src):
        if os.path.isfile(src + '/' + filename):
            fin = open(src + '/' + filename)
            print "Current file: " + filename
            text = fin.read()
            # start = time.time()
            dic = nlp_get_words(text, sent_detector, pstemmer, tagger)
            gen_term_freq(dic, filename)
            # total_time = time.time() - start
            # print total_time

# Return the words that got from the nlp algo
# Any change regarding the nlp should be done here...
def nlp_get_words(text, sent_detector, pstemmer, tagger):
    import string
    ascii_text = text.strip().encode("ascii", "ignore").lower()

    sentences = sent_detector.tokenize(ascii_text)
    dic = {}
    for sentence in sentences:
        try:
            w = nltk.word_tokenize(sentence)
            tags = tagger.tag(w)
            used_tags = ['NN.*', 'VB.*', 'JJ.*', 'RB.*']
            # NN = Nouns
            # VB = Verbs
            # JJ = Adjectives
            # RB = Adverbs
            reqd_tags = "(" + ")|(".join(used_tags) + ")"
            reqd_words = [re.sub("[!#$=*+',%]", '', a) for (a, b) in tags if re.match(
                reqd_tags, b) and re.match('[a-z].*', a)]
            stemmed_words = [pstemmer.stem(a) for a in reqd_words]
            # print reqd_words
            for string in stemmed_words:
                if string in dic:
                    dic[string] += 1
                else:
                    dic[string] = 1
        except Exception, e:
            print "Error", e
    return dic


def gen_term_freq(dic, filename):
    folder_name = 'tfreq-nltk/' + args.directory
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    wr = open("%s/%s" % (folder_name, filename), 'w')
    json.dump(dic, wr, indent=2)
    wr.close()

#
# if __name__ == "__main__":
#     dirname = args.directory
#     dirpath = '../dat/' + dirname
#     sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#     traverse(sent_detector, dirpath)
