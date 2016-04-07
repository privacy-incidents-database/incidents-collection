import json
import requests
import os
import sys
import urllib2
# use this package to get rid of the html and js tags.
import getopt
import argparse
import hashlib


def get_args():
    global args
    parser = argparse.ArgumentParser(description="Script for collecting urls for NYTimes articles")
    parser.add_argument('-k', '--keywords', nargs = '+', metavar = 'N', help = 'Keywords for fetching the Articles')
    parser.add_argument('-l', '--limit', type = int, help = 'Limit of the number of Articles to be fetched, must be a multiple of 10')
    parser.add_argument('-j', '--json',type = str, help = 'Name of the Json file containing the urls')

    args = parser.parse_args()
    return args

def get_keywords():
    keywords = args.keywords
    keywordstr = ""
    cnt = 0

    if keywords is not None:
        for keyword in keywords:
            keywordstr += keyword
            if cnt < len(keywords) - 1 :
                keywordstr += "+"
            cnt += 1

    return keywordstr


API_KEY = os.environ.get("NY_TIMES_API_KEY")
args = get_args()
keywordstr = get_keywords()
abstractindex = 0

def collect():
    url = build_url(0)
    r = requests.get(url)
    if r.status_code == 200:
        w = r.json()
        if w.has_key('response'):
            hits = w['response']['meta']['hits']
            print "Number of articles for the current Query = " + str(hits)
            if hits > 0:
                if args.limit is not None:
                    if args.limit < hits:
                        hits = args.limit

                get_articles(hits)


def build_url(pageno):
    if not keywordstr:
        url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?&page=" \
        + str(pageno) + "&api-key=" + API_KEY
    else:
        url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + keywordstr + \
        "&page=" + str(pageno) + "&api-key=" + API_KEY
    return url

def get_articles(hits):
    dict = {}
    global abstractindex
    cnt = 0
    while cnt < hits:
        if cnt%10 == 0:
            pageno = cnt/10
            url = build_url(pageno)
            r = requests.get(url)

        if r.status_code == 200:
            w = r.json()
            if w.has_key('response'):

                docs = w['response']['docs']
                for d in docs:
                    cnt += 1
                    if d['web_url'] is not None:
                        info = {}
                        if not keywordstr:
                            info["type"] = 3

                        if keywordstr == "Security":
                            info["type"] = 2

                        elif keywordstr == "Computer+Security":
                            info["type"] = 1

                        info["url"] = d["web_url"]
                        dict[hashlib.sha1(d['web_url']).hexdigest()] = info

                if not keywordstr:
                    fname = "input/random.json"

                if keywordstr == "Security":
                    fname = "input/security.json"

                if keywordstr == "Computer+Security":
                    fname = "input/CompSec.json"

                json.dumps(dict)
                fp = open(fname, 'w')
                json.dump(dict, fp, indent = 2)




collect()
