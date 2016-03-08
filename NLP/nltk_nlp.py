#-*- coding: utf-8 -*-
import nltk.data
import re
import pprint
import os
import time
import sys
import json
import argparse
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

args = get_args()

def traverse(src):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    tagger = PerceptronTagger()
    pstemmer = PorterStemmer()

    for filename in os.listdir(src):
        if os.path.isfile(src + '/' + filename):
            fin = open(src + '/' + filename)
            print "Current file: " + filename
            text = fin.read()
            # start = time.time()
            dic = get_count(text, sent_detector, pstemmer, tagger)
            genTermFreq(dic, filename)
            # total_time = time.time() - start
            # print total_time


def get_count(text, sent_detector, pstemmer, tagger):
    import string
    asciitext = text.strip().encode("ascii", "ignore").lower()
    # asciitext = asciitext.translate(string.maketrans(" "," "),string.punctuation)

    sentences = sent_detector.tokenize(asciitext)
    dic = {}
    for sentence in sentences:
        try:
            w = nltk.word_tokenize(sentence)
            tags = tagger.tag(w)
            # print tags
            usedTags = ['NN.*', 'VB.*', 'JJ.*', 'RB.*']
            # NN = Nouns
            # VB = Verbs
            # JJ = Adjectives
            # RB = Adverbs

            reqdTags = "(" + ")|(".join(usedTags) + ")"

            reqdWords = [a for (a, b) in tags if re.match(
                reqdTags, b) and re.match('[a-z].*', a)]

            # Stem the required words

            stemmedWords = [pstemmer.stem(a) for a in reqdWords]

            # print reqdWords
            for string in stemmedWords:
                if dic.has_key(string):
                    dic[string] += 1
                else:
                    dic[string] = 1
        except Exception, e:
            print "Error"
        # a = raw_input()
    # pprint.pprint(dic)
    return dic


def genTermFreq(dic, filename):
    folderName = 'tfreq-nltk/' + args.directory
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    wr = open("%s/%s" % (folderName, filename), 'w')
    json.dump(dic, wr, indent=2)
    wr.close()


if __name__ == "__main__":
    dirname = args.directory
    dirpath = '../dat/' + dirname
    traverse(dirpath)
