import csv
import json
import sys
import os
import pprint
import re
import argparse


def get_args():
    global args
    parser = argparse.ArgumentParser(
        description="Script for generating CSV from articles in Given directories")
    parser.add_argument("library", help='Name of the Library used for NLP')
    args = parser.parse_args()
    return args

args = get_args()


def gen_csv(neg, pos):
    """
    Generate CSV according to the json stored.
    neg: path to negative directory
    pos: path to postive directory

    """
    fin = open('tfid-log-' + args.library + '.csv', 'rb')
    idfreader = csv.reader(fin)

    idfkey = []
    idfval = []
    rowcnt = 0
    for row in idfreader:
        if rowcnt == 0:
            idfkey = row
        elif rowcnt == 2:
            idfval = row
        rowcnt += 1

    # Build idf dictionary
    idfdic = dict(zip(idfkey, idfval))

    fout = open('tfidf-' + args.library + '.csv', 'w')
    out = csv.writer(fout)

    # output = cStringIO.StringIO()
    # out = csv.writer(output)

    src = [neg, pos]
    dic = ['no.', 'isPrivacy']
    length = len(dic)
    keywords = []

    # Get all the keywords
    for s in src:
        for filename in os.listdir(s):
            fin = open(s + '/' + filename)
            dat = json.load(fin)
            for key in dat:
                if key not in keywords:
                    keywords.append(key)

    keywords = sorted(keywords)
    # pprint.pprint(keywords)
    # a = raw_input()
    dic.extend(keywords)

    # sorted and write as header
    rank = [0] * (len(keywords))
    out.writerow(dic)
    cnt = 1
    for s in src:
        # pos and neg src
        for filename in os.listdir(s):
            # filename => every file in the directory
            fin = open(s + '/' + filename)
            dat = json.load(fin)
            print "Current File: " + filename

            for key, val in dat.iteritems():
                try:
                    idfdic[key]
                except Exception, e:
                    idfdic[key] = 1

                rank[keywords.index(key)] = val * float(idfdic[key])

            flag = 0
            if s == pos:
                flag = 1
            result = [cnt,flag]
            result.extend(rank)

            out.writerow(result)
            rank = [0] * (len(keywords))
            cnt += 1
            fin.close()


gen_csv('tfreq-' + args.library + '/NYnegative',
        'tfreq-' + args.library + '/content')
