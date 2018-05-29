#!/usr/bin/python
import sys
from math import log

if __name__=='__main__':
	idf={}
	num_of_docs=0.0
	document_lemmata=set()
	for line in sys.stdin:
		line=line.strip()
		if line=='':
			for lemma in document_lemmata:
				idf[lemma]=idf.get(lemma,0)+1
			num_of_docs+=1
			document_lemmata=set()
		else:
			document_lemmata.add(line)
	for lemma,freq in sorted(idf.items(),reverse=True,key=lambda x:x[1]):
		sys.stdout.write(lemma+'\t'+str(round(log(num_of_docs/freq,2),4))+'\n')
