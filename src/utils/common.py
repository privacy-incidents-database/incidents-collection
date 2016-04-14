import os
import json

# Remove the non-ascii characters in a text file
# @input text
# @return text
def remove_non_ascii(s):
    import string
    printable = set(string.printable)
    s = filter(lambda x: x in printable, s)
    return s


def traverse(func):
    def new_function(*args):
        dic = args[0]
        src = args[1]
        for filename in os.listdir(src):
            if os.path.isfile(src + '/' + filename):
                fin = open(src + '/' + filename)
                text = fin.read()
                func(dic, text)

    return new_function


@traverse
def show_word(dic, text):
    dat = json.loads(text)
    for key in dat:
        dic[key] = dat[key]


@traverse
def count_word(dic, text):
    dat = json.loads(text)
    for key in dat:
        if key in dic:
            dic[key] += dat[key]
        else:
            dic[key] = dat[key]


def get_words_frequency(func, folder):
    dic = {}
    func(dic, folder)
    return dic

