#!/usr/bin/env python
import glob
import mincemeat
import re



files = glob.glob('hw3data/*')

def contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

source = dict((file_name, contents(file_name))
              for file_name in files)


def mapfn(k, v):
    for line in v.splitlines():
        data = re.split(r":{2,3}", line)
        title = data[-1].split()
        for author in data[1:-1]:
            w = {}
            for word in title:
                if word.lower() not in allStopWords:
                    if word.lower() in w.keys():
                        w[word.lower()] = w[word.lower()]+1
                    else:
                        w[word.lower()] = 1
            yield author, w

def reducefn(k, v):
    w = {}
    s = {}
    for words in v:
        for word in words.keys():
            if word.lower() in w.keys():
                w[word.lower()] = w[word.lower()]+1
            else:
                w[word.lower()] = 1
    s = sorted(w.iteritems(), key=operator.itemgetter(1))
    return s

s = mincemeat.Server()
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print results

