import json
import requests
import os
def collect():
    API_KEY=os.environ.get("NY_TIMES_API_KEY")
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=privacy+leakage&api-key="+API_KEY
    r = requests.get(url)
    if r.status_code == 200 :
        w = r.json()
        if w.has_key('response'):
            docs =  w['response']['docs']
            for d in docs:
                if d['abstract'] is not None:
                    print "Abstract:", d['abstract']
                    print "keyword:",
                    for keyword in d['keywords']:
                         print keyword['value'].lower(),"|||",
                    print "\n"
    else:
        print r
collect()