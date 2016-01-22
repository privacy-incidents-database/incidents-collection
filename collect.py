import json
import requests
import os
import sys
import urllib2
# use this package to get rid of the html and js tags.
import getopt
from bs4 import BeautifulSoup

def getkeywords():
    keywords = sys.argv[1:]
    keywordstr = ""
    cnt = 0

    for keyword in keywords:
        keywordstr += keyword
        if cnt < len(keywords) - 1 :
            keywordstr += "+"
        cnt += 1

    return keywordstr

# Global variables
API_KEY = os.environ.get("NY_TIMES_API_KEY")
keywordstr = getkeywords()
abstractindex = 0

def collect():

    url = buildurl(0)
    r = requests.get(url)
    if r.status_code == 200:
        w = r.json()
        if w.has_key('response'):
            hits = w['response']['meta']['hits']
            print "Number of articles for the current Query = " + str(hits)
            if hits > 0:
                getarticles(hits)

def buildurl(pageno):
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + keywordstr + \
    "&page=" + str(pageno) + "&fl=abstract,byline,headline,web_url,word_count&api-key=" + API_KEY
    return url

def getarticles(hits):
    global abstractindex
    cnt = 0
    while(cnt < hits):
        if cnt%10 == 0:
            pageno = cnt/10
            url = buildurl(pageno)
            r = requests.get(url)

        if r.status_code == 200:
            w = r.json()
            if w.has_key('response'):
                docs = w['response']['docs']
                for d in docs:
                    if d['web_url'] is not None and d['headline']['main'] is not None:
                        cnt += 1
                        #Extract the file name from the url
                        filename = d['web_url'].rsplit('/',1)[1]
                        filename = filename.rsplit('.',1)[0]
                        if filename == "abstract":
                            filename = filename + str(abstractindex)
                            abstractindex += 1
                            #  Ignore files named abstract, No textual content
                            continue

                        print "Fetching Article: " + filename

                        try:
                            # use urllib2 to read the html content instead of using
                            # wget to fetch local
                            response = urllib2.urlopen(d['web_url'])
                            html = response.read()
                            clean(html, d['headline']['main'], filename)


                        except Exception, e:
                            print e
                            print "not valid"




def clean(string, headline, filename):
    remove_tag = clean_html(string)  # remove tags
    whtml = open("html/%s.txt" % filename, 'w')
    whtml.write(remove_tag.encode('utf-8') + "\n")
    # find start point according to lead_paragraph
    headline = headline + "\n\n\nBy"
    remove_tag = remove_tag.lower()
    headline = headline.lower()
    start = remove_tag.find(headline)
    # start = start + len(headline)
    #start = remove_tag.find(headline, start)
    remove_start = remove_tag[start:]  # start from the lead para_graph
    # mark the end using string Inside NYTimes.com
    end = remove_start.find("inside nytimes.com")

    final = remove_start[:end].rstrip()  # final ver

    wr = open("webpage/%s.txt" % filename, 'w')  # write into txt file.
    wr.write(final.encode('utf-8') + "\n")
    return final


def clean_html(fragment):
    soup = BeautifulSoup(fragment, 'html.parser')
    return soup.get_text()



collect()
