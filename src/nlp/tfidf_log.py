import csv, json, os, math
import argparse
from utils.common import get_words_frequency


def get_args():
    global args
    parser = argparse.ArgumentParser(
        description="Script for generating CSV from articles in Given directories")
    parser.add_argument("library", help='Name of the Library used for NLP')
    args = parser.parse_args()
    return args

args = get_args()


def gen_csv(neg, pos, keywords):
    """
    Generate CSV according to the json stored.
    neg: path to negative directory
    pos: path to postive directory

    """
    fout = open('tfid-log-' + args.library + '.csv', 'w')
    out = csv.writer(fout)
    if keywords is None:
        src = [neg, pos]
        keywords = {}
        ##Get all the keywords
        for s in src:
            temp = get_words_frequency(s)
            keywords.update(temp)
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
    
gen_csv('tfreq-' + args.library + '/content','tfreq-' + args.library + '/NYnegative')
