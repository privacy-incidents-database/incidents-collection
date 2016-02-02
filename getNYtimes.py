import json

with open('urls/url.json') as data_file:
    out = []
    data = json.load(data_file)
    for d in data:
        url = str(d['link'])
        if "nytimes.com" in url:
            out.append(d)

    fp = open("urls/nytimes.json", 'w')
    json.dump(out, fp, indent = 2)
