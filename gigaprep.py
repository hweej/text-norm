#!/usr/bin/python
"""
Usage:

python gigaprep.py -in <path to files directory> OR <singular file>

python gigaprep.py -in "/data/*.xml.gz" OR /data/xin_eng_199501.xml.gz

"""
#Decompress xml gz file
#Extract each <P> from text body <TEXT> of each story ducment <DOC type="story">
#For each paragraph, apply sentence tokenization
#For each sentence, apply Penn Treebank word tokenizer

#Remove all tokens which are not purely alphabetic or which occur in the NLTK
#stopword list

#Stem all remaining tokens using the Porter stemmer
#Finally, convert all tokens to uppercase and print each sentence to standard out

import gzip
import argparse
import glob
import re

from lxml import etree
from nltk.tokenize.punkt import PunktSentenceTokenizer 
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

def processFile(fh):
    with gzip.open(fh, 'rb') as f:
        tree = etree.parse(f)
        root = tree.getroot()        
        r = re.compile('^[a-zA-Z]+$')
        s = SnowballStemmer("english")

        paragraphs = root.xpath('DOC[@type="story"]/TEXT/P')        
        
        for p in paragraphs:            
            try:
                sentences = PunktSentenceTokenizer().sentences_from_text(p.text)

                for sentence in sentences:                
                    tokens = TreebankWordTokenizer().tokenize(sentence)

                    #Filter by alphabetic only
                    alphabetic = filter(r.match, tokens)
                    #Filter by stopwords & stem all leftover tokens
                    stop_filtered = [s.stem(w) for w in alphabetic if w.lower() not in stopwords.words('english')]

                    print (" ").join(stop_filtered).upper()
            except:
                continue        


    return True

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument('-in')

    args = parser.parse_args()

    for doc in glob.glob(getattr(args, 'in')):
        processFile(doc)
    
    



