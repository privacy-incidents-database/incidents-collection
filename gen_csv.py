import csv,json,sys,os
def gen_csv(neg,pos):
    """
    Generate CSV according to the json stored.
    neg: path to negative directory
    pos: path to postive directory
    
    """
    fout = open('data.csv','w')
    out = csv.writer(fout)
    dic = ['no.','type_of_material','news_desk','word_count','keywords','document_type','pub_date','byline','isPrivacy'];
    src = [neg,pos]
    out.writerow(dic)
    cnt = 1
    for s in src:
        ###pos and neg src
        for filename in os.listdir(s):
            ###filename => every file in the directory
            fin = open(s+'/'+filename)
            dat = json.load(fin)
            for i in range(1,len(dic)-1):
                try:
                    #valid json, key
                    dat[dic[i]]
                except Exception,e:
                    print e
                    ##inject none if key doesn't exists
                    dat[dic[i]]='none'
                finally:
                    ###list item
                    if dic[i] == 'keywords':
                        string = ''
                        for st in dat['keywords']:
                            string = string + st['value'] + ','
                        dat['keywords'] = string[0:len(string)-1]
                    if dic[i] == 'byline':
                        string = ''
                        people =  dat['byline']['person']
                        for person in people:
                            try:
                                lastname = person['lastname']
                                firstname = person['firstname']
                                lastname.encode('ascii')
                                firstname.encode('ascii')
                                name = firstname.title() + ' ' + lastname.title()
                            except Exception,e:
                                try:
                                    name = person['original']
                                except Exception,e:
                                    # print person
                                    name = 'none'
                            string = string + name + ','
                        #to ascii since there are some Spanish name
                        string.encode('ascii')
                        dat['byline'] = string[0:len(string)-1]
                    try:
                        dat[dic[i]] = str(dat[dic[i]])
                    except Exception, e:
                        print dat[dic[i]] 
            flag = False
            if s == pos:
                flag = True
            out.writerow([cnt,dat['type_of_material'].lower(),dat['news_desk'].lower(),dat['word_count'].lower(),dat['keywords'].lower(),dat['document_type'].lower(),dat['pub_date'].lower(),dat['byline'],flag])
            cnt+=1
            fin.close()
gen_csv('dat/NYnegative/json','dat/NYpositive/json')
    
