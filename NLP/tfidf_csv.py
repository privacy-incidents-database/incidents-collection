import csv,json,sys,os,pprint,re
def gen_csv(neg,pos):
    """
    Generate CSV according to the json stored.
    neg: path to negative directory
    pos: path to postive directory

    """
    fin = open('tfid-log-spacy.csv','rb')
    idfreader = csv.reader(fin)

    idfkey = []
    idfval = []
    rowcnt = 0
    for row in idfreader:
        if rowcnt == 0:
            idfkey = row
        elif rowcnt == 2:
            idfval = row
        rowcnt += 1

    #Build idf dictionary
    idfdic = dict(zip(idfkey,idfval))


    fout = open('tfidf-spacy.csv','w')
    out = csv.writer(fout)
    src = [neg,pos]
    dic = ['no.','filename','isPrivacy']
    length = len(dic)
    keywords = []

    ##Get all the keywords
    for s in src:
        for filename in os.listdir(s):
            fin = open(s+'/'+filename)
            dat = json.load(fin)
            for key in dat:
                if key not in keywords:
                    keywords.append(key)

    dic.extend(sorted(keywords))

    ##sorted and write as header
    rank = [0] * (len(keywords))
    out.writerow(dic)
    cnt = 1
    for s in src:
        ###pos and neg src
        for filename in os.listdir(s):
            ###filename => every file in the directory
            fin = open(s+'/'+filename)
            dat = json.load(fin)
            # print "Current File: " + filename

            for key,val in dat.iteritems():
                try:
                    idfdic[key]
                except Exception,e:
                    idfdic[key] = 1

                rank[sorted(keywords).index(key)] = val*float(idfdic[key])


            flag = False
            if s == pos:
                flag = True
            result = [cnt,filename,flag]
            result.extend(rank)

            out.writerow(result)
            rank = [0]*(len(keywords))
            cnt+=1
            fin.close()

gen_csv('tfreq-spacy/NYnegative','tfreq-spacy/content')
