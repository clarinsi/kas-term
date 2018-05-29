#!/usr/bin/python
import os,sys
reldir = os.path.dirname(os.path.abspath(__file__))
file = sys.argv[1]
patterns = sys.argv[2]
idf = sys.argv[3]
for stat in ('chisq','dice','ll','mi','tscore','tfidf'):
    print '## statistic',stat
    for l in range(4):
        if l == 0 and stat != 'tfidf':
            continue
        print '# length',l+1
        if stat == 'tfidf':
            print 'python ' + os.path.join(reldir, 'CollTerm.py') + ' -seq 2 -p ' + patterns + ' -i ' + file + ' -m ' + stat + ' -l ' + str(l + 1) + ' -pos 0 3 2 -idf ' + idf + ' -norm 1 > ' + file + '.' + stat + '.' + str(l + 1)
            os.system('python ' + os.path.join(reldir, 'CollTerm.py') + ' -seq 2 -p ' + patterns + ' -i ' + file + ' -m ' + stat + ' -l ' + str(l + 1) + ' -pos 0 3 2 -idf ' + idf + ' -norm 1 > ' + file + '.' + stat + '.' + str(l + 1))
        else:
            print 'python ' + os.path.join(reldir, 'CollTerm.py') + ' -seq 2 -p ' + patterns + ' -i ' + file + ' -m ' + stat + ' -l ' + str(l + 1) + ' -pos 0 3 2 -norm 1 > ' + file + '.' + stat + '.' + str(l + 1)
            os.system('python ' + os.path.join(reldir, 'CollTerm.py') + ' -seq 2 -p ' + patterns + ' -i ' + file + ' -m ' + stat + ' -l ' + str(l + 1) + ' -pos 0 3 2 -norm 1 > ' + file + '.' + stat + '.' + str(l + 1))
