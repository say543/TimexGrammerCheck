from collections import Counter, OrderedDict

import json
import sys
import random
import math

import xml.etree.cElementTree as ET


import sys

#from numpy import array



#from itertools import izip
#import zip
class TimexGrammerCheck:

    @classmethod
    def GetTimeXCanonicalValue(cls, queryTagMocks):

        startTag = "<TIMEX3";
        endTag = "</TIMEX3>";


        res = []
        index = 0 
        while index < len(queryTagMocks):
            try:   
                si = queryTagMocks.index(startTag, index);
                sj = queryTagMocks.index(endTag, index);

                #res.append(queryTagMocks[si:sj+len(endTag)]);
                #print (queryTagMocks[si:sj+len(endTag)]);
                # http://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/processing-xml-in-python-with-element-tree.html
                res.append((queryTagMocks[si:sj+len(endTag)], ET.fromstring(queryTagMocks[si:sj+len(endTag)].replace("\\",""))));

                index = sj+len(endTag);
            except ValueError:
                break;

        return res


if __name__ == '__main__':
        
    
    print ('executing...')
    # queryfile
    queryFileName = None
    intFileName = None
    prodFileName = None
    diffFileName = None
    queryFile = None
    intFile = None
    prodFile = None
    diffFile = None

    startTag = "<TIMEX3"
    endTag = "</TIMEX3>"

    try:
        total = len(sys.argv)
        # https://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/
        # argument list examples
        # -q ..\\reminder-training-45K.tsv  -i ..\\int\\reminder-training-45K.Generated.tsv -p ..\\prod\\reminder-training-45K.Generated.tsv -o ..\\diff.tsv
        argLen = len(sys.argv)
        # skip the executive file
        i = 1
        while i < argLen:
            if (sys.argv[i] == "-q" and i+1 < argLen):
                queryFileName = sys.argv[i+1]
                i = i+2
            elif (sys.argv[i] == "-i" and i+1 < argLen):
                intFileName = sys.argv[i+1]
                i = i+2
            elif (sys.argv[i] == "-p" and i+1 < argLen):
                prodFileName = sys.argv[i+1]
                i = i+2
            elif (sys.argv[i] == "-o" and i+1 < argLen):
                diffFileName = sys.argv[i+1]
                i = i+2
            else:
                i = i+1

        # input file example
        #queryFile = open("..\\reminder-training-45K.tsv", "r")
        #intFile = open("..\\int\\reminder-training-45K.Generated.tsv", "r")
        #prodFile = open("..\\prod\\reminder-training-45K.Generated.tsv", "r")
        # outfile example 
        #diffFile = open("..\\diff.tsv", "w")
        if queryFileName is None:
            raise ValueError("miss -q queryFileName")
        if intFileName is None:
            raise ValueError("miss -i intFileName")
        if prodFileName is None:
            raise ValueError("miss -d prodFileName")
        if diffFileName is None:
            raise ValueError("miss -o diffFileName")

        queryFile = open(queryFileName, "r")
        intFile = open(intFileName, "r")
        prodFile = open(prodFileName, "r")
        diffFile = open(diffFileName, "w")

        index = 1;
        for line1, line2, line3 in zip(intFile, prodFile, queryFile):

            res = ""

            line1Parts = line1.split("\t");
            line2Parts = line2.split("\t");
            line3Parts = line3.split("\t");

            #if index == 126:
            #    print("for debug")
            #print (index)

            if line1Parts[2] != line2Parts[2]:
                res += line3Parts[4] +"\t" + "C"+ str(index);
                #diffFile.write(res+"\n");
                line1Ind = 0;
                line2Index = 0;
                
                line1Timex = TimexGrammerCheck.GetTimeXCanonicalValue(line1Parts[2])
                line2Timex = TimexGrammerCheck.GetTimeXCanonicalValue(line2Parts[2])


                if (len(line1Timex) != len(line2Timex)):
                    res += "\t"+ ''.join(map(lambda x: (x[0]) ,  line1Timex)) + "\t" + ''.join(map(lambda x: (x[0]) ,  line2Timex));
                else:
                    for tuple1, tuple2 in zip(line1Timex , line2Timex):

                       # comparing span if they are the same  
                       #if (tuple1[1].text != tuple2[1].text):
                       #    res += "\t"+ tuple1[0] + "\t" + tuple2[0];
                       if (tuple1[0] != tuple2[0]):
                           res += "\t"+ tuple1[0] + "\t" + tuple2[0];


                #for timex in line1Timex:
                #    print (timex[1].text)
                #res = line1Timex == line2Timex

                #print (res)
                diffFile.write(res+"\n");

            index = index +1;
            #print("int = %s, prod = %s" % \
            #(line1, line2))

    except ValueError as excep:
        print ("input argument in valid: %s" % (excep))
    except Exception:
        print ("unknown exception, something wrong")
    finally:
        if queryFile is not None:
            queryFile.close()
        if intFile is not None:
            intFile.close()
        if prodFile is not None:
            prodFile.close()
        if diffFile is not None:
            diffFile.close()

