from collect import fetch_url as fetch
from collect import clean as clean
from collect import clean_html as clean_html
import json


def get_content_from_json():
    """
    generate content from input json
    """
    with open('urls/url.json') as data_file:
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
                raw_html = fetch(url)
                if raw_html is not None:
                    clean(raw_html, filename=filename)
            except Exception, e:
                print "Not successful url", url
                print e
    print "finished"

get_content_from_json()