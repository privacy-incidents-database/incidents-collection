from collect import fetch_url as fetch
from collect import clean as clean
from collect import clean_html as clean_html
import json


def get_content_from_json():
    """
    generate content from input json
    """
    with open ('urls/url.json') as data_file:
        data = json.load(data_file)
        for d in data:
            meta_data = {}
            meta_data['filename'] = d['Descr']
            url = d['link']
            raw_html = fetch(url)
            clean(raw_html)
            # final = clean_html(raw_html)
            # wr = open("webpage/%s.txt" % "jesse", 'w')  # write into txt file.
            # wr.write(url+"\n")
            # wr.write(final.encode('utf-8') + "\n")
            # break


def test():
    with open('webpage/jesse.txt') as data_file:
        data = data_file.read()
        print data.find("NHS-accredited health apps found to be sending unencrypted personal information")


get_content_from_json()
# test()