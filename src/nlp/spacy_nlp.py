from spacy.en import English
import os, json, re


parser = English()


# def traverse(src):
#     for filename in os.listdir(src):
#         if os.path.isfile(src+'/'+filename):
#             fin = open(src+'/'+filename)
#             text = fin.read()
#             words = nlp_get_words(parser, text)
#             fout = open(src.replace('../dat/','tfreq-spacy/') + '/' + filename,'w')
#             json.dump(words,fout,indent=2)
#             fout.close()
#
        
        
# Return the words that got from the nlp algo
def nlp_get_words(parser, text):
    nouns = {}
    adj = {}
    adv = {}
    verbs = {}
    try:
        # multi_sentence = unicode(text, encoding="ascii")
        parsed_data = parser(text)
        for span in parsed_data.sents:
            sent = [parsed_data[i] for i in range(span.start, span.end)]
            for token in sent:
                if re.match('[a-zA-Z]{2,}',token.lemma_):
                    if token.pos_ == 'NOUN':
                        if token.lemma_ not in nouns:
                            nouns[token.lemma_] = 1
                        else:
                            nouns[token.lemma_] +=1
                    elif token.pos_ == 'VERB':
                        if token.lemma_ != '':
                            if token.lemma_ not in verbs :
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
        words = nouns.copy()
        words.update(adj)
        words.update(adv)
        words.update(verbs)
        return words
    except Exception, e:
        print "error", e

# traverse('../dat/NYnegative')
# traverse('../dat/content')
# pprint.pprint(nouns)

