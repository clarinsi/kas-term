#!/usr/bin/python
import sys
import os
reldir=os.path.dirname(os.path.abspath(__file__))
mwt_factor=1.
swt_factor=1.
file=sys.argv[1]
X_idx={}
for line in open(file+'.tfidf.1'):
    lemma,seq,patfreq,statval=line.split('\t')
    statval=float(statval)
    pattern,freq=patfreq[1:-1].split(', ')
    lemma=lemma+'\t'+seq+'\t'+pattern
    X_idx[lemma]={}
    X_idx[lemma]['tfidf']=statval
    X_idx[lemma]['avgtoklen']=len(seq)
    if lemma not in X_idx:
        continue
terms=X_idx.keys()
X=[X_idx[e] for e in terms]
from sklearn.externals import joblib
clf=joblib.load(os.path.join(reldir,'model.swt'))
labels=[]
decisions=[]
if len(X)!=0:
    decisions=list(clf.decision_function(X)*swt_factor)
    labels=list(clf.predict(X))
X_idx={}
for length in range(2,5):
    for stat in ('dice','chisq','ll','mi','tscore','tfidf'):
        for line in open(file+'.'+stat+'.'+str(length)):
            lemma,seq,patfreq,statval=line.split('\t')
            statval=float(statval)
            pattern,freq=patfreq[1:-1].split(', ')
            lemma=lemma+'\t'+seq+'\t'+pattern
            if stat=='dice':
                X_idx[lemma]={}
                X_idx[lemma]['frequency']=freq
                #X_idx[lemma]['pattern']=pattern
            if lemma not in X_idx:
                continue
            X_idx[lemma][stat]=statval
terms2=X_idx.keys()
terms.extend(terms2)
X=[X_idx[e] for e in terms2]
from sklearn.externals import joblib
clf=joblib.load(os.path.join(reldir,'model.mwt'))
if len(X)!=0:
    decisions.extend(clf.decision_function(X)*mwt_factor)
    labels.extend(clf.predict(X))
for term,prob,response in sorted(zip(terms,decisions,labels),key=lambda x:-x[1]):
    sys.stdout.write(term+'\t'+str(prob)+'\n')
