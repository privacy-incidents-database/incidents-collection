import json
import requests
import os
import sys
import urllib2
# use this package to get rid of the html and js tags.
import getopt
from bs4 import BeautifulSoup

def get_keywords():
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
                get_articles(hits)


def build_url(pageno):
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + keywordstr + \
    "&page=" + str(pageno) + "&fl=abstract,byline,headline,web_url,word_count&api-key=" + API_KEY
    return url


def get_articles(hits):
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
                    if d['web_url'] is not None and d['headline']['main'] is not None:
                        cnt += 1
                        #Extract the file name from the url
                        filename = d['web_url'].rsplit('/', 1)[1]
                        filename = filename.rsplit('.', 1)[0]
                        if filename == "abstract":
                            filename = filename + str(abstractindex)
                            abstractindex += 1
                            #  Ignore files named abstract, No textual content
                            continue

                        print "Fetching Article: " + filename
                        metadata={}
                        metadata['filename'] = filename
                        metadata['headline'] = d['headline']['main']
                        html = fetch_url(d['web_url'])
                        clean(html, headline=metadata['headline'], filename=metadata['filename'])


def fetch_url(url):
    """
    @param string url
    @return string raw_html
    """
    try:
    # use urllib2 to read the html content instead of using
    # wget to fetch local
    # Add cookie to solve 303 problem.
        from cookielib import CookieJar
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(url)
        html = response.read()
        return html
    except Exception, e:
        print e
        print "Not successful url", url


def clean(string, **kwargs):
    """
    @param string raw_html
    @param dict
        headline: headline of news
        filename: filename of the output file
    @return
    """
    headline = kwargs.get('headline')
    filename = kwargs.get('filename')
    remove_tag = clean_html(string)  # remove tags
    if headline is not None or remove_tag.lower().find(filename) != -1:
        if remove_tag.lower().find(filename) != -1:
            headline = filename
        headline += "\n\n\nBy"
        remove_tag = remove_tag.lower()
        headline = headline.lower()
        start = remove_tag.find(headline)
        remove_start = remove_tag[start:]  # start from the lead para_graph
        # mark the end using string Inside NYTimes.com
        end = remove_start.find("inside nytimes.com")
        final = remove_start[:end].rstrip()  # final ver
    else:
        # # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in remove_tag.splitlines())
        # # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # # drop blank lines
        final = '\n'.join(chunk for chunk in chunks if len(chunk) > 50) #if chunk is longer than 50 chars, think it is valid.
        # find start point according to lead_paragraph
    wr = open("content/%s.txt" % filename, 'w')  # write into txt file.
    wr.write(final.encode('utf-8') + "\n")
    # return final


def clean_html(fragment):
    """
    @param string raw_html
    @return string html_with plain text
    """
    soup = BeautifulSoup(fragment, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()

    return text


collect()
