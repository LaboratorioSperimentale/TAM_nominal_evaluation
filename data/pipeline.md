The present folder collects data processed for the presentation at SLI2024 (September 2024 - Catania).

The code used to process data can be found at: https://github.com/LaboratorioSperimentale/TAM_nominal_evaluation
More specifically, refer to release 2.0 for reproducibility: https://github.com/LaboratorioSperimentale/TAM_nominal_evaluation/releases/tag/2.0

In what follows, we'll describe the steps that were performed.

1. **Clone the repo** from https://github.com/LaboratorioSperimentale/TAM_nominal_evaluation and navigate to main folder

2. **Create a virtual environment** and install the required dependencies by running
	```
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	```

3. Create `logs` and `data` folder
   ```
   mkdir logs
   mkdir data
   ```

   The data folder can be organized in various ways, you'll see a number of subfolder used in the commands. Those have to be created explicitly before running the commands

4. **Input corpora**
   As input data, we took into consideration the Repubblica Corpus, the wikiConLL dump and ITWaC Corpus.
   Repubblica is unfortunately not freely available, wikiconll can be downloaded from [here](), for the latter contact wacky@sslmit.unibo.it
   Paths to files containing corpora, in the conll format as described in the [repository](https://github.com/LaboratorioSperimentale/TAM_nominal_evaluation), need to be stored in a file formatted as described in `data_sample/files_input.tsv`

   Therefore, create `files_input.tsv` in `data/` and add local paths to where you stored the resources on your machine.

5. **Compute `NOUN` frequencies**

   As a first step, we compute frequencies of tokens bearing a `NOUN` part of speech tag by running:

   ```
   python3 main.py frequencies -i files_input.tsv -o data/noun_frequencies
   ```


6. **Merge and sort step**

   Noun frequencies computed over various sources are then merged into a single file by running:

   ```
   python3 main.py merge -i data/noun_frequencies -o data/noun_frequencies -p nouns --output-filename merged.tsv
   ```

   For better human readibility (i.e., this step is optional), this file is then sorted from command line by running:

   ```
   sort -nr data/noun_frequencies/merged.tsv > data/noun_frequencies/merged.sorted.tsv
   ```

   From manual inspection of file `data/noun_frequencies/merged.sorted.tsv`, we set 100 as a minimun frequency threshold on nouns for the next steps.


7. **Extract compounds and ngrams**

   We run the extraction of both TAM compounds and syntactic ngrams by running:

   ```
   python3 main.py extract -i files_input.tsv --type ngram  -o data/ngrams_frequencies --nouns-filename data/noun_frequencies/merged.tsv -t 100
   ```

   ```
   python3 main.py extract -i files_input.tsv --type compound  -o data/compound_frequencies --nouns-filename data/noun_frequencies/merged.tsv -t 100
   ```


8. **Merge and sort step**

   As for step (3), we then merged and sorted frequencies coming from different sources.
   This is now done in 4 steps as:
   - for the compound case, frequencies of nouns and prefixes are extracted
   - for the ngram case, frequencies of nouns and adverbs are extracted

   Therefore we run:

   ```
   python3 main.py merge -i ngrams_frequencies -o ngrams_frequencies -p nouns --output-filename nouns_merged.tsv
   ```
   ```
   python3 main.py merge -i ngrams_frequencies -o ngrams_frequencies -p adverbs --output-filename adverbs_merged.tsv
   ```

   ```
   python3 main.py merge -i compound_frequencies -o compound_frequencies -p nouns --output-filename nouns_merged.tsv
   ```
   ```
   python3 main.py merge -i compound_frequencies -o compound_frequencies -p prefs --output-filename prefs_merged.tsv
   ```

   Each of the produced frequency files is then sorted for better manual inspection, by running:


   ```
   sort -nr ngrams_frequencies/nouns_merged.tsv > ngrams_frequencies/nouns_merged.sorted.tsv
   ```
   ```
   sort -nr ngrams_frequencies/adverbs_merged.tsv > ngrams_frequencies/adverbs_merged.sorted.tsv
   ```

   ```
   sort -nr compound_frequencies/nouns_merged.tsv > compound_frequencies/nouns_merged.sorted.tsv
   ```
   ```
   sort -nr compound_frequencies/prefs_merged.tsv > compound_frequencies/prefs_merged.sorted.tsv
   ```
9. **Selection of adverbs and prefixes**

   We restricted the choice of adverbs and prefixes to a small subset of interesting cases. (min freq 30 for prefixes and 10 for adverbs)

   The selected elements are stored in files:
   - `compound_frequencies/prefs_selected.tsv`
   - `ngrams_frequencies/adverbs_selected.tsv`


#########################





7. **Extraction of contexts**

   For the selected prefixes and adverbs, contexts are extracted from original sources by running:

   ```
   python3 main.py contexts -i files_input.tsv --type compound -o compound_contexts --accepted-nouns compound_frequencies/nouns_merged.tsv --nouns-threshold 5 --accepted-prefs compound_frequencies/prefs_selected.tsv --prefs-threshold 0 -c 20
   ```

   ```
   python3 main.py contexts -i files_input.tsv --type ngram -o ngrams_contexts --accepted-nouns ngrams_frequencies/nouns_merged.tsv --nouns-threshold 5 --accepted-adverbs ngrams_frequencies/adverbs_selected.tsv --adverbs-threshold 0 -c 20
   ```


8. **Sampling of contexts**

   In order to perform semantic annotation, a subset of maximum 20 contexts per noun was selected by running:

   ```
   python3 main.py sample -i ngrams_contexts -o ngrams_samples -s 32 -n 20
   ```

   ```
   python3 main.py sample -i compound_contexts -o compound_samples -s 76 -n 20
   ```


9. **Annotation**

	The sampled contexts were then sorted into folders `compound_annotated` and `ngrams_annotated`.
	For each context, a label was manually associated to the base noun, following the ontology described in `ontology.md`
