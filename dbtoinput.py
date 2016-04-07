import json, hashlib

with open('urls/url.json') as data_file:
    dict = {}
    data = json.load(data_file)
    for d in data:
        info = {}
        info["type"] = 0
        info["url"] = d["link"]
        dict[hashlib.sha1(d['link']).hexdigest()] = info

    json.dumps(dict)
    fp = open("input/positive.json", 'w')
    json.dump(dict, fp, indent = 2)
