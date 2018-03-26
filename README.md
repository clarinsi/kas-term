# kas-term - a supervised terminology extractor

kas-term extracts terms with their statistics from documents in an annotated corpus,
using a MSD (PoS) pattern file,
and a lexicon of manually annotated terms. 

This terms extractor is a supervised learning extension to
the unsupervised terminnology extractor CollTerm.
To train the models, CollTerm should be applied over each corpus document, to produce the models then used
by the kas-term supervised extension, resulting in a final ranked list of term candidates.

The included example covers Slovene academic writing. The models were computed from the KAS corpus (http://nl.ijs.si/kas/) of PhD theses, and one example thesis is included.

## CollTerm

### CollTerm background resources

The input to CollTerm is an annotated corpus and two additional files:
- a pattern file specifying the morphosyntactic patterns of term candidates
(exemplary Slovene file is ```example/patterns.txt```)
- a file with IDF weights of relevant lemmas (the exemplary Slovene file is ```example/kas.idf```,
and calculated on the whole KAS, to downplay the general academic terminology such as "thesis" or "chapter")

The script ```calculate_idf.py``` is used to generate the IDF weights of lemmas.
From standard input it reads a list of lemmas,
with empty lines encoding document boundaries.
A toy example calculated on the example thesis ```example/kas-9916```,
assuming that pages are actually documents (as this is one single document), is:

```
$ sed 's/<\/page>//g' example/kas-9916 | grep -v '^<' | cut -f 3 | tr [:upper:] [:lower:] | python calculate_idf.py
in	0.0344
,	0.0444
.	0.0697
v	0.1429
(	0.2428
)	0.2428
na	0.2777
z	0.3074
biti	0.3317
socialen	0.4594
...
```

### Running CollTerm.py

For running CollTerm.py as a standalone tool, you should run it with
python2.7 without arguments and go through its help prompt.

If you use CollTerm just for feature extraction for the supervised
terminology extraction, you should run the handy
```extract_features.py``` script in case your data is encoded in a
similar fashion to the examplary ```example/kas-9916``` file. You
might need to adjust the ```-pos``` flag otherwise (```positions of
tokens, POS tags and lemmas (zero-based indices)```).

The example of running the script on the ```example/kas-9916``` file is this:

```
python extract_features.py example/kas-9916 example/patterns.txt example/kas.idf
```

The extracted term candidates with the corresponding weights are extracted to the same path as the input file, with extensions defining the statistic and length of the candidates.

## Supervised terminology extraction

### Running the supervised extractor

Once you have features extracted with the CollTerm.py tool, you can apply the prebuilt models to obtain a single list of candidates, ranked by the certainty of the classifier.

The values in the output of the ```rank_terms.py``` are
- the lemma sequence of the term candidate
- the most frequent surface sequence of the term candidate
- the classifier decision whether this is a term or not
- the certainty of the classifier (ranking criterion)

```
$ python rank_terms.py example/kas-9916
mreženje	mreženje	1	1.17892204408
internet	interneta	1	1.14913593709
starostnica	starostnic	1	1.13324548116
prijatelj	prijatelji	1	1.10347914906
starostnik	starostniki	1	1.06736899811
izoliranost	izoliranosti	1	1.05143794863
vključevanje	vključevanja	1	1.0203457586
računalnik	računalnika	1	1.019743232
socialen kapital	socialni kapital	1	1.01835208519
socialen omrežje	socialna omrežja	1	1.01489046515
spleten klepetalnica	spletnih klepetalnic	1	1.01300463806
...
```

Notice that two different models - the single-word term (SWT) and the multi-word term (MWT) models are applied separately and their outputs are merged and sorted by the certainty criterion. This makes SWT candidates always take highest positions, which is questionable. You might consider introducing a factor either for SWT or MWT candidates in the ```rank_terms.py``` script. There are two variables for that at the beggining of the script, called ```swt_factor``` and ```mwt_factor```.

### Training the supervised extractor

For training the supervised extractor, there are the python2.7 ```train_swt.py``` and ```train_mwt.py``` scripts prepared. The human annotations on Slovene academic texts from the KAS project, together with the CollTerm-relevant statistics, are available in the ```kas.term.json``` file.

## Citing our work

If using the CollTerm tool you should cite
```
@inproceedings{pinnis12-term,
Author = {M{\=a}rcis Pinnis and Nikola Ljube{\v s}i{\'c} and Dan {\c S}tef{\u a}nescu and Inguna Skadi{\c n}a and Marko Tadi{\'c} and Tatiana Gornostay},
Booktitle = {Proceedings of the Terminology and Knowledge Engineering (TKE2012) Conference},
Title = {Term Extraction, Tagging, and Mapping Tools for Under-Resourced Languages},
Year = {2012}}
```

A paper describing the supervised approach to terminology extraction is waiting on a busy-bee colleague of mine.
