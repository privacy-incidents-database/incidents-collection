#-*- coding: utf-8 -*-
import nltk.data
import re
import pprint
import os
import time
import sys
import json
from nltk.stem.porter import *

def traverse(src):
    cnt = 0
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    pstemmer = PorterStemmer()

    for filename in os.listdir(src):
        if os.path.isfile(src+'/'+filename):
            fin = open(src+'/'+filename)
            print "Current file: " + filename
            text = fin.read()
            start = time.time()
            dic = get_count(text, sent_detector, pstemmer)
            genTermFreq(dic, filename)
            total_time = time.time() - start
            print total_time
            cnt+=1
    print cnt

def get_count(text,sent_detector,pstemmer):
    import string
    asciitext = text.strip().decode("ascii","ignore").encode("ascii").lower()
    asciitext = asciitext.translate(string.maketrans(" "," "),string.punctuation)

    sentences = sent_detector.tokenize(asciitext)
    dic ={}
    for sentence in sentences:
        try:
            w = nltk.word_tokenize(sentence)
            tags = nltk.pos_tag(w)
            # print tags
            usedTags = ['NN.*','VB.*','JJ.*','RB.*']
            # NN = Nouns
            # VB = Verbs
            # JJ = Adjectives
            # RB = Adverbs

            reqdTags = "("+")|(".join(usedTags)+")"

            reqdWords = [a for (a, b) in tags if re.match(reqdTags, b) and re.match('[a-z].*',a)]

            # Stem the required words

            stemmedWords = [pstemmer.stem(a) for a in reqdWords]

            # print reqdWords
            for string in stemmedWords:
                if dic.has_key(string):
                    dic[string] += 1
                else:
                    dic[string] = 1
        except Exception,e:
            print "Error"
        # a = raw_input()
    # pprint.pprint(dic)
    return dic

def genTermFreq(dic, filename):
    folderName = 'tfreq/' + sys.argv[1]
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    wr = open("%s/%s" % (folderName,filename), 'w')
    json.dump(dic , wr, indent = 2)
    wr.close()

def stanfordNERExtractor(sentence):
    from nltk.tag.stanford import NERTagger
    st =  NERTagger('/usr/share/stanford-ner/classifiers/all.3class.distsim.crf.ser.gz',
               '/usr/share/stanford-ner/stanford-ner.jar')
    return st.tag(sentence.split())


if __name__ == "__main__":
        dirname = sys.argv[1]
        dirpath = '../dat/' + dirname
        traverse(dirpath)
