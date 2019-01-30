from collections import Counter, OrderedDict

import json
import sys
import random
import math

import xml.etree.cElementTree as ET


import sys


import re


if __name__ == '__main__':
        
    
    print ('executing...')

    intFileName = None
    diffFileName = None
    intFile = None
    diffFile = None

    try:
        spanOnly = False
        total = len(sys.argv)
        # https://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/
        # argument list examples
        # -i ..\\int\\reminder-training-45K.Generated.tsv -o ..\\diff.tsv
        argLen = len(sys.argv)
        # skip the executive file
        i = 1
        while i < argLen:

            if (sys.argv[i] == "-i" and i+1 < argLen):
                intFileName = sys.argv[i+1]
                i = i+2
            elif (sys.argv[i] == "-o" and i+1 < argLen):
                diffFileName = sys.argv[i+1]
                i = i+2

        # input file example
        #queryFile = open("..\\reminder-training-45K.tsv", "r")
        #diffFile = open("..\\diff.tsv", "w")
        if intFileName is None:
            raise ValueError("miss -i intFileName")
        if diffFileName is None:
            raise ValueError("miss -o diffFileName")

        intFile = open(intFileName, "r",  encoding="utf8")
        diffFile = open(diffFileName, "w")
        
        queryInd = 0
        for lineWithEnd in zip(intFile):
            try:
                outputStr = ""
                line = lineWithEnd[0][:-1]

                i = 0
                pattern = re.compile("<(.*?)>(.*?)<\/.*?>")
                for m in pattern.finditer(line):
                    matchIndex = m.start()

                    if (matchIndex - i > 0):
                        strs = line[i:matchIndex].strip()
                        if len(strs) >0:
                            for str in strs.split("\s"):
                                outputStr += f"{str.strip()}\tO\n"
                                #diffFile.write (f"{str.strip()}\tO\n")

                    annotation = re.search(pattern, m.group())
                    #print(annotation.group(2).strip())
                    #print(annotation.group(1).strip())
                    outputStr += f"{annotation.group(2).strip()}\t{annotation.group(1).strip()}\n"
                    #diffFile.write (f"{annotation.group(2).strip()}\t{annotation.group(1).strip()}\n")

                    i = matchIndex + len(m.group())
                if i < len(line):
                    strs = line[i:len(line)].strip()
                    if len(strs) >0:
                        for str in strs.split("\s"):
                            outputStr += f"{str}\tO\n"
                            #diffFile.write (f"{str}\tO\n")
                            #diffFile.write (f"{str.strip()}\tO\n")

                # end of one query
                #diffFile.write (f"\n")
                outputStr += f"\n"
                diffFile.write(outputStr)
                queryInd = queryInd +1

            except ValueError as excep:
                print (f"skip input argument in valid: {queryInd} {lineWithEnd} {excep}")
    except Exception:
        print (f"unknown exception, something wrong")
    finally:
        if intFile is not None:
            intFile.close()
        if diffFile is not None:
            diffFile.close()
