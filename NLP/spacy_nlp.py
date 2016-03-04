#-*- coding: utf-8 -*-
from spacy.en import English
import os,json
import pprint,string
parser = English()

nouns={}
adj={}
adv={}
verbs={}

def traverse(src):
    for filename in os.listdir(src):
        if os.path.isfile(src+'/'+filename):
            words = {}
            fin = open(src+'/'+filename)
            text = fin.read()
            nlp(text)
            fout = open("tfreq-spacy/content/%s" % filename,'w')
            words= nouns.copy()
            words.update(adj)
            words.update(adv)
            words.update(verbs)
            adj.clear()
            adv.clear()
            nouns.clear()
            verbs.clear()
            json.dump(words,fout,indent=2,)
            fout.close()
        
        
def nlp(text):
    try:
        multiSentence = unicode(text,encoding="utf-8")
        printable = set(string.printable)
        filter(lambda x: x in printable, multiSentence)
    # all you have to do to parse text is this:
    #note: the first time you run spaCy in a file it takes a little while to load up its modules
        parsedData = parser(multiSentence)
        # Let's look at the sentences
        sents = []
        # the "sents" property returns spans
        # spans have indices into the original string
        # where each index value represents a token
        # for span in parsedData.sents:
        #     # go from the start to the end of each span, returning each token in the sentence
        #     # combine each token using join()
        #     sent = ''.join(parsedData[i].string for i in range(span.start, span.end)).strip()
        #     sents.append(sent)
        #
        #
        # Let's look at the part of speech tags of the first sentence

        for span in parsedData.sents:
            sent = [parsedData[i] for i in range(span.start, span.end)]
            for token in sent:
                if token.pos_== 'NOUN':
                    if token.lemma_ not in nouns:
                        nouns[token.lemma_] = 1
                    else:
                        nouns[token.lemma_] +=1
                elif token.pos_== 'VERB':
                    if token.lemma_ not in verbs:
                        verbs[token.lemma_] = 1
                    else:
                        verbs[token.lemma_] +=1
                elif token.pos_ == 'ADJ':
                    if token.lemma_ not in adj:
                        adj[token.lemma_] = 1
                    else:
                        adj[token.lemma_] +=1
                elif token.pos_ == 'ADV':
                    if token.lemma_ not in adv:
                        adv[token.lemma_] = 1
                    else:
                        adv[token.lemma_] +=1
        
    except Exception,e:
        print "error"

traverse('../dat/content')
pprint.pprint(nouns)
