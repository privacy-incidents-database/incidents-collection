import sys
import csv
import time
import json
import hashlib

dict = {}

def getjson():
    fname = sys.argv[1]
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            info = {}

            if row[2].lower() == "negative":
                info["type"] = 4
            elif row[2].lower() == "positive":
                info["type"] = 0
            else:
                info["type"] = "TBD"

            info["url"] = row[1]

            dict[hashlib.sha1(info["url"]).hexdigest()] = info

            json.dumps(dict)
            fp = open("input/csvinput.json", 'w')
            json.dump(dict, fp, indent = 2)
    # print dict

getjson()
