#-*- coding: utf-8 -*-
from spacy.en import English
import os 
parser = English()

nouns={}
orgs={}
verbs={}

def traverse(src):
    for filename in os.listdir(src):
        fin = open(src+'/'+filename)
        text = fin.read()
        nlp(text)
def nlp(text):
    try:
        multiSentence = unicode(text,encoding="ascii")    
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
                elif token.ent_type_ == 'ORG':
                    if token.ent_type_ not in orgs:
                        orgs[token.ent_type_] = 1
                    else:
                        orgs[token.ent_type_] +=1
                # print(token.lemma_, token.pos_,token.ent_type_)
    except Exception,e:
        print "error"

traverse('../dat/content')
print nouns

