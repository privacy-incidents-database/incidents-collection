import os 
def remove_non_ascii(s):
    import string
    printable = set(string.printable)
    s = filter(lambda x: x in printable, s)
    return s
def traverse(src):
    for filename in os.listdir(src):
        if os.path.isfile(src+'/'+filename):
            fin = open(src+'/'+filename)
            text = fin.read()
            text = remove_non_ascii(text)
            fout = open(src+'/'+filename,'w')
            fout.write(text)
traverse("dat/content")
traverse("dat/NYnegative")