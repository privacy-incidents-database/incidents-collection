import csv,json,sys,os,math,re
import argparse

def get_args():
    global args
    parser = argparse.ArgumentParser(
        description="Script for generating CSV from articles in Given directories")
    parser.add_argument("library", help='Name of the Library used for NLP')
    args = parser.parse_args()
    return args

args = get_args()

def gen_csv(neg,pos):
    """
    Generate CSV according to the json stored.
    neg: path to negative directory
    pos: path to postive directory

    """
    fout = open('tfid-log-' + args.library + '.csv','w')
    out = csv.writer(fout)
    src = [neg,pos]
    # length = len(dic)
    keywords = {}

    ##Get all the keywords
    for s in src:
        for filename in os.listdir(s):
            fin = open(s+'/'+filename)
            dat = json.load(fin)
            for key in dat:
                if key in keywords:
                    keywords[key] += 1
                else:
                    keywords[key] = 1
    # dic.extend(sorted(keywords))
    ##sorted and write as header
    out.writerow(sorted(keywords.keys()))
    val = []
    for key in sorted(keywords.keys()):
        val.append(keywords[key])
    out.writerow(val)
    log_val = []
    length = len(val)
    for v in val:
        log_val.append(float(math.log10(length/v)))
    out.writerow(log_val)
    fin.close()

gen_csv('tfreq-' + args.library + '/content','tfreq-' + args.library + '/NYCompSec')
