from collect import fetch_url as fetch
from collect import clean as clean
from collect import clean_html as clean_html
from collect import get_args
import json
import sys
import os
import requests

args = get_args()

def get_content_from_json():
    """
    generate content from input json
    """

    with open('urls/%s' % args.json) as data_file:
        data = json.load(data_file)
        for d in data:
            try:
                url = str(d['link'])
                if url.startswith("http") == False and url.startswith("https") == False:
                    url = "http://"+url
                filename = str(d['Descr'].lower())
                filename = filename.encode('utf-8')
                filename = filename.translate(None, '!@#$/\\')
                if len(filename) > 50:
                    filename = filename[0:50]

                if args.json == 'nytimes.json':
                    create_json(url, filename)

                raw_html = fetch(url)
                if raw_html is not None:
                    clean(raw_html, filename=filename)
            except Exception, e:
                print "Not successful url", url
                print e
    print "finished"

def create_json(web_url, filename):
    API_KEY = os.environ.get("NY_TIMES_API_KEY")


    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?callback=svc_search_v2_articlesearch \
    &fq=web_url:%22"+web_url+"%22&api-key=""" + API_KEY
    print "Fetching Article: " + web_url

    query = web_url
    query = query.rsplit('/')[-1]
    query = query.split('.html')[0]

    # print "Fetching Article: " + query
    url2 = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + query \
    + "&api-key=" + API_KEY

    r = requests.get(url)
    if r.status_code == 200:
        w = r.json()
        if w.has_key('response'):
            docs = w['response']['docs']
            if not docs:
                r2 = requests.get(url2)
                if r2.status_code == 200:
                    w = r2.json()
                    if w.has_key('response'):
                        docs = w['response']['docs']

            for d in docs:
                if query in d['web_url']:
                    folderName = args.destination
                    if not os.path.exists(folderName):
                        os.makedirs(folderName)

                    jsonFolder = folderName + "/json"
                    if not os.path.exists(jsonFolder):
                        os.makedirs(jsonFolder)

                    #Write json
                    wr = open("%s/json/%s.json" % (folderName,filename), 'w')
                    json.dump(d , wr, indent = 2)
                    wr.close()

if __name__ == "__main__":
    get_content_from_json()
