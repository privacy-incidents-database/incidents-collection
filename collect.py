import json
import requests
import os
import sys
def collect():
    import urllib2
    API_KEY=os.environ.get("NY_TIMES_API_KEY")
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=privacy+leakage&page=0&fl=abstract,byline,lead_paragraph,web_url,word_count&api-key=" + API_KEY
    r = requests.get(url)
    if r.status_code == 200 :
        w = r.json()
        if w.has_key('response'):
            docs =  w['response']['docs']
            i = 0
            for d in docs:
                if d['web_url'] is not None and d['lead_paragraph'] is not None:
                    try:
                        # use urllib2 to read the html content instead of using wget to fetch local
                        response = urllib2.urlopen(d['web_url'])
                        html = response.read()
                        clean(html,d['lead_paragraph'],i)
                        i+=1#indexing
                    except Exception,e:
                        print e
                        print "not valid"
                
                        
        print r
def clean(string,lead_para,index):
    def clean_html( fragment ):
        from bs4 import BeautifulSoup#use this package to get rid of the html and js tags.
        soup = BeautifulSoup(fragment, 'html.parser')
        return soup.get_text()
    remove_tag = clean_html(string)#remove tags
    start = remove_tag.find(lead_para[0:50])#find start point according to lead_paragraph
    remove_start = remove_tag[start:]#start from the lead para_graph
    end = remove_start.find("\n\n\n\n")#mark the end using 4 continuous endline
    final = remove_start[:end]#final ver
    wr = open("webpage/%s.txt" % index,'w')#write into txt file.
    wr.write(final+"\n")
    return final
    
collect()
