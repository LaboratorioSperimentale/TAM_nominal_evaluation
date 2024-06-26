# Temporal, Aspectual, Modal evaluation of reference

- [Temporal, Aspectual, Modal evaluation of reference](#temporal-aspectual-modal-evaluation-of-reference)
	- [Repository structure](#repository-structure)
	- [Data sources](#data-sources)
		- [ItWaC](#itwac)
			- [Annotation](#annotation)
			- [Sample input](#sample-input)
		- [Repubblica](#repubblica)
			- [Annotation](#annotation-1)
			- [Sample input](#sample-input-1)
		- [WikiCoNLL](#wikiconll)
			- [Annotation](#annotation-2)
			- [Sample input](#sample-input-2)
	- [Processing steps](#processing-steps)
		- [`frequencies`](#frequencies)
		- [`merge`](#merge)
		- [`extract`](#extract)
		- [`contexts`](#contexts)
		- [`sample`](#sample)
	- [Future steps](#future-steps)
		- [itTenTen](#ittenten)
		- [refactor](#refactor)


## Repository structure

This repository contains code and sample data used for the study "Temporal, aspectual and modal evaluation of reference"

The folder is structured as follows:
1. subfolder `data_sample` contains samples of input and output data used in the study. Cases will be explained in this README
2. subfolder `logs` is the default output folder for python loggers
3. `TAM` contains the main library
4. `main.py` contains the code that is actually runnable


In order to run the code you should:
1. create a virtual environment (`python > 3.11` is recommended)
2. install packages listed in `requirements.txt`
3. activate your virtual environment
4. run `main.py -h` to know which functionalities are available (also described below)


## Data sources

The present code is able to handle multiple data sources: a sample for each one can be found in the folder `data_sample/corpora/`.

The overall aim is to evaluate nominal modification by means of:
- prefixation (through hyphenation)
- syntactic collocation

For full functionality, the code relies on [Universal Dependencies](https://universaldependencies.org/) tagsets, both for part of speech labels and for dependency annotation.

More specifically, the code requires:
- _nouns_ to be tagged as `NOUN`
- _adverbs_ to be tagged as `ADV`
- _adjectives_ to be tagged ad `ADJ`
- _determiners_ to be tagged as `DET`

As far as dependency relations are concerned, no check is done on dependency label names, but the code expects the noun to be the head both in the noun-determiner relation and in the noun-adverb relation.

The code is currently supporting three kind of input sources, formatted as described in the following subsections.

More sources and formats can be easily integrated by adding a `reader_X` function in the `utils.py` module. Consequently, the `utils.read` function should be appropriately modified by adding another if-condition.

The new `reader_X` function should yield `Sentences` (as described in the `objects` module) populated by `Token` objects. Each `Token` should be initialized with information about its `id` within the sentence, `form`, `lemma`, `part of speech` and optionally `head` (can be set to `-1` if unavailable) and `dependency relation` (can be set to `""` if unavailable).


### ItWaC

Info from [WaCKy project](https://wacky.sslmit.unibo.it/doku.php?id=corpora): a 2 billion word corpus constructed from the Web limiting the crawl to the .it domain and using medium-frequency words from the Repubblica corpus and basic Italian vocabulary lists as seeds.


#### Annotation

PoS Tags: [https://sslmit.unibo.it/~baroni/collocazioni/itwac.tagset.txt](https://sslmit.unibo.it/~baroni/collocazioni/itwac.tagset.txt)

For the purpose of this study, we performed the following mapping (only relevant categories) from native PoS tagging to UD:

| Original |  UD    |
| -----    |  ----- |
| ADJ      |  ADJ   |
| ADV      |  ADV   |
| ART      | DET    |
| ARTPRE   | DET    |
| NEG      | ADV    |
| DET:demo | DET    |
| DET:indef| DET    |
| DET:num  | DET    |
| DET:poss | DET    |
| DET:wh   | DET    |
| NOUN     | NOUN   |
| DET      |  X     |

No syntactic annotation is provided.


#### Sample input

```
<corpus>
<text id="http://www3.varesenews.it/varese/articolo.php?id=9627">
<s>
-	PUN	-
Nel	ARTPRE	nel
1980	NUM	@card@
la	ART	la
provincia	NOUN	provincia
di	PRE	di
Varese	NPR	Varese
aiutò	VER:fin	aiutare
il	ART	il
paese	NOUN	paese
dell'	ARTPRE	dell'
Irpinia	NPR	Irpinia
.	SENT	.
</s>
```

### Repubblica

Info from [DIT UniBO](https://docs.sslmit.unibo.it/doku.php?id=corpora:repubblica): The “la Repubblica” corpus is a very large corpus of Italian newspaper text (approximately 380M tokens).


#### Annotation

For the purpose of this study, we performed the following mapping (only relevant categories) from native PoS tagging to UD:

| Original |  UD    |
| -----    |  ----- |
| A        |  ADJ   |
| B        |  ADV   |
| EA       |  DET   |
| DD       |  DET   |
| DI       |  DET   |
| DE       |  DET   |
| DQ       |  DET   |
| DR       |  DET   |
| RD       |  DET   |
| R        |  DET   |
| S        |  NOUN  |



#### Sample input

```
<text id="1">
<s>
1       I       il      R       RD      num=p|gen=m     2       det     _       _
2       SEGRETI segreto S       S       num=p|gen=m     0       ROOT    _       _
3       DELLA   di      E       EA      num=s|gen=f     2       comp    _       _
4       NATO    Nato    S       SP      _       3       prep    _       _
5       .       .       F       FS      _       2       punc    _       _
</s>
<s>
1       È       essere  V       V       num=s|per=3|mod=i|ten=p 0       ROOT    _       _
2       ABBASTANZA      ABBASTANZA      S       SP      _       1       subj    _       _
3       strano  strano  A       A       num=s|gen=m     2       mod     _       _
4       il      il      R       RD      num=s|gen=m     5       det     _       _
5       disinteresse    disinteresse    S       S       num=s|gen=m     1       pred    _       _
6       con     con     E       E       _       10      comp    _       _
7       cui     cui     P       PR      num=n|gen=n     6       prep    _       _
8       è       essere  V       VA      num=s|per=3|mod=i|ten=p 9       aux     _       _
9       stata   essere  V       VA      num=s|mod=p|gen=f       10      aux     _       _
10      accolta accogliere      V       V       num=s|mod=p|gen=f       5       mod_rel _       _
11      l'      il      R       RD      num=s|gen=n     12      det     _       _
12      intervista      intervista      S       S       num=s|gen=f     10      subj    _       _
13      che     che     P       PR      num=n|gen=n     19      subj    _       _
14      l'      l'      P       PC      num=s|per=3|gen=n       19      comp_ind        _       _
15      on.     on.     S       SA      _       17      mod     _       _
16      Rino    Rino    S       SP      _       17      mod     _       _
17      Formica Formica S       SP      _       19      subj    _       _
18      ha      avere   V       VA      num=s|per=3|mod=i|ten=p 19      aux     _       _
19      dato    dare    V       V       num=s|mod=p|gen=m       12      mod_rel _       _
20      sabato  sabato  S       S       num=s|gen=m     19      obj     _       _
21      scorso  scorso  A       A       num=s|gen=m     20      mod     _       _
22      alla    al      E       EA      num=s|gen=f     19      comp_loc        _       _
23      Repubblica      Repubblica      S       SP      _       22      prep    _       _
24      .       .       F       FS      _       1       punc    _       _
</s>
```

### WikiCoNLL

Info from [WaCKy project](https://wacky.sslmit.unibo.it/doku.php?id=corpora): semantically and syntactically annotated Italian Wikipedia

#### Annotation

For the purpose of this study, we performed the following mapping (only relevant categories) from native PoS tagging to UD:

| Original |  UD    |
| -----    |  ----- |
| A        |  ADJ   |
| B        |  ADV   |
| EA       |  DET   |
| DD       |  DET   |
| DI       |  DET   |
| DE       |  DET   |
| DQ       |  DET   |
| DR       |  DET   |
| RD       |  DET   |
| R        |  DET   |
| S        |  NOUN  |



#### Sample input

```
<doc id="2" url="http://it.wikipedia.org/wiki/Armonium">
1	Armonium	Armonium	S	SP	_	0	ROOT	_	_	O	O
2	.	.	F	FS	_	1	punc	_	_	O	O

1	L'	il	R	RD	num=s|gen=n	2	det	_	_	O	O
2	armonium	armonium	S	S	num=n|gen=m	13	subj	_	_	O	B-noun.act
3	o	o	C	CC	_	2	dis	_	_	O	O
4	armonio	armonio	S	S	num=s|gen=m	2	disj	_	_	O	B-noun.act
5	(	(	F	FB	_	6	punc	_	_	O	O
6	in	in	E	E	_	13	comp	_	_	O	O
7	francese	francese	A	A	num=s|gen=n	6	prep	_	_	O	B-adj.all
8	,	,	F	FF	_	6	punc	_	_	O	O
9	"	"	F	FB	_	10	punc	_	_	O	O
10	harmonium	harmonium	S	S	num=n|gen=m	6	conj	_	_	O	B-noun.person
11	"	"	F	FB	_	10	punc	_	_	O	O
12	)	)	F	FB	_	6	punc	_	_	O	O
13	è	essere	V	V	num=s|per=3|mod=i|ten=p	22	arg	_	_	O	B-verb.stative
14	uno	uno	R	RI	num=s|gen=m	15	det	_	_	O	O
15	strumento	strumento	S	S	num=s|gen=m	13	pred	_	_	O	B-noun.artifact
16	musicale	musicale	A	A	num=s|gen=n	15	mod	_	_	O	B-adj.pert
17	azionato	azionare	V	V	num=s|mod=p|gen=m	15	mod	_	_	O	O
18	con	con	E	E	_	17	comp	_	_	O	O
19	una	uno	R	RI	num=s|gen=f	20	det	_	_	O	O
20	tastiera	tastiera	S	S	num=s|gen=f	18	prep	_	_	O	B-noun.act
21	,	,	F	FF	_	13	punc	_	_	O	O
22	detta	dettare	V	V	num=s|per=3|mod=i|ten=p	0	ROOT	_	_	O	O
23	manuale	manuale	A	A	num=s|gen=n	22	pred	_	_	O	B-adj.all
24	.	.	F	FS	_	22	punc	_	_	O	O
```


## Processing steps

### `frequencies`

Computes frequency of `NOUN` tokens.

Usage:
```
python3 main.py frequencies
	-i [path/to/input_files_list.tsv]
	-o [path/to/output/folder]
```

An example of `input_files_list` is provided in the `data_sample` folder.

Only nouns composed by alphabetic characters are considered, or characters in the set `(-, ., " ")`, but at least on character has to be alphabetic.

### `merge`

Merges frequencies lists.

Usage:

```
python3 main.py merge
	-i [path/to/input/folder]
	-o [path/to/output/folder]
	-p pattern
	--output-filename file_basename

```

The script will merge all files that match pattern `path/to/input/folder/*pattern*` into file `path/to/output/folder/file_basename`

### `extract`
Extracts both prefixed nouns and syntactic ngrams from source corpora.

Usage:
```
python3 main.py extract
	-i [path/to/input_files_list.tsv]
	-o [path/to/output/folder]
	--type [compound|ngram]
	--nouns-filename [path/to/file/with/nouns/frequencies]
	-t threshold on nouns frequencies
```

The script only considers:
- compounds where the base noun has frequency greater than threshold
- ngrams where the apprearing noun has frequency greater than threshold

### `contexts`

Extracts left and right contexts for both prefixed compounds and syntactic ngrams.

Usage:
```
python3 contexts
	-i [path/to/input_files_list.tsv]
	-o [path/to/output/folder]
	--type [compound|ngram]
	-c left|right context width (in tokens)
	--accepted-nouns [path/to/file/with/nouns/frequencies]
	--accepted-prefs [path/to/file/with/prefixes/frequencies]
	--accepted-adverbs [path/to/file/with/adverbs/frequencies]
	--nouns-threshold threshold on nouns frequencies
	--prefs-threshold threshold on prefixes frequencies
	--adverbs-threshold threshold on adverbs frequencies
```

### `sample`

Samples a fixed number of contexts per noun maintaining the proportion among different sources.

Usage:
```
python3 main.py sample
	-i [path/to/input/folder]
	-o [path/to/output/folder]
	-s random seed for reproducibility
	-n number of contexts to sample
```

## Future steps

### itTenTen

Available through SketchEngine API, add script `sketchengine_api.py`

### refactor

extract and contexts share too much code, they need refactoring