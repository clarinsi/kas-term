#-*-coding:utf8-*-
#additional MWT features
from sklearn.metrics import roc_auc_score,roc_curve,auc,classification_report
from sklearn.svm import SVC,SVR,LinearSVR
from sklearn.linear_model import SGDRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import LeaveOneGroupOut
from math import log
import json
import numpy as np
from scipy.stats import spearmanr
clf2=Pipeline([('dv',DictVectorizer(sparse=False)),('scl',StandardScaler()),('clf',SVC(class_weight='balanced',probability=True))])
#inclusive mapping
coarse_map={u'n_nerelevantno': 0., u'x_izvenpodro\u010dni': 1., u'z_znanstveno': 1., 't_termin':1.}
#exclusive mapping
#coarse_map={u'n_nerelevantno': 0., u'x_izvenpodro\u010dni': 0., u'z_znanstveno': 0., 't_termin':1.}
y=[]
X=[]
for entry in json.load(open('kas.term.json')):
  if entry['length']>1:
    y.append(np.mean([coarse_map[entry['annotator_'+str(i+1)]] for i in range(4)]))
    x={}
    for stat in ('frequency','dice','chisq','ll','mi','tscore','tfidf'):
      x[stat]=entry[stat]
    x['pattern']=entry['pattern']
    X.append(x)
if False:
#if add_pattern:
  from sklearn.feature_extraction import DictVectorizer
  import pandas as pd
  dv=DictVectorizer(sparse=False) 
  df=pd.DataFrame(X).convert_objects(convert_numeric=True)
  X=dv.fit_transform(df.to_dict(orient='records'))
y_cat=[1 if e>=0.5 else 0 for e in y]
X=np.array(X)
y_cat=np.array(y_cat)
clf2.fit(X,y_cat)
from sklearn.externals import joblib
joblib.dump(clf2,'model.mwt')