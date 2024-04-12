import collections
import tqdm

import utils

def extract_ctx_advN(filename, source, file_id, accepted_prefs, accepted_nouns, ctx, output_files):

	for sentence in tqdm.tqdm(utils.read(filename, source)):
		candidates = {}
		for tok_id, token in enumerate(sentence.sentence):
			if token.pos == "NOUN" and "-" in token.form:
				formsplit = token.form.rsplit("-", 1)
				if formsplit[1] in accepted_nouns and formsplit[0] in accepted_prefs:
					candidates[tok_id] = (formsplit[0], formsplit[1])

		for candidate, compound in candidates.items():

			prefix, noun = compound

			sentence_portion_left = sentence.sentence[max(0, candidate-ctx):candidate]
			sentence_portion_right = sentence.sentence[candidate+1:min(len(sentence.sentence), candidate+ctx+1)]

			ctx_left = " ".join([token.form for token in sentence_portion_left])
			candidate_str = sentence.sentence[candidate].form
			ctx_right = " ".join([token.form for token in sentence_portion_right])

			if not prefix in output_files:
				output_files[prefix] = open(f"../data/output/{prefix}.contexts.tsv", "w")

			print(f"{source}\t{prefix}\t{noun}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=output_files[prefix])


def extract_ctx_detADVN(filename, source, file_id, accepted_nouns, accepted_adverbs, ctx, output_files):


	for sentence in tqdm.tqdm(utils.read(filename, source)):
		candidates = {}

		for tok_id, token in enumerate(sentence.sentence):
			if token.pos == "ADV" and token.form in accepted_adverbs and \
				tok_id > 2 and \
					tok_id < len(sentence.sentence)-2:
					candidates[tok_id] = token


		for c_id, adverb_object in candidates.items():
			
			sentence_portion_left = None
			sentence_portion_right = None

			# adverb_object = sentence.sentence[c_id]
			
			pprevious_object = sentence.sentence[c_id-2]
			previous_object = sentence.sentence[c_id-1]
			
			next_object = sentence.sentence[c_id+1]
			nnext_object = sentence.sentence[c_id+2]
			
			if previous_object.pos == "DET":                                                # DET ADV ? ? case

				sentence_portion_left = sentence.sentence[max(0, c_id-1-ctx):c_id-1]

				determiner_object = previous_object
				
				if (
					next_object.pos == "NOUN" and next_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == adverb_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == next_object.id))
				):                                                                          # DET ADV NOUN case
					
					noun_object = next_object
					ngramtype = "DET ADV NOUN"

					sentence_portion_right = sentence.sentence[c_id+2:min(len(sentence.sentence), c_id+2+ctx+1)]
					occurrence = sentence.sentence[c_id-1:c_id+2]
					

					# if noun_object.form in accepted_nouns:
					# 	freqs[(adverb_object.form, noun_object.form)] += 1
					# 	adverbs_freqs[adverb_object.form] += 1
					# 	nouns_freqs[noun_object.form] += 1

						
						# freqs[(determiner_object.form, adverb_object.form, noun_object.form)] += 1
						


				elif (
					next_object.pos == "ADV" and \
					nnext_object.pos == "NOUN" and nnext_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == nnext_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == nnext_object.id) or \
					(next_object.deprel == "" or next_object.head == nnext_object.id))
				):                                                                          # DET ADV ADV NOUN case
					
					noun_object = nnext_object
					adverb_object.form = adverb_object.form + " " + next_object.form
					ngramtype = "DET ADV NOUN"
					sentence_portion_right = sentence.sentence[c_id+3:min(len(sentence.sentence), c_id+3+ctx+1)]
					occurrence = sentence.sentence[c_id-1:c_id+3]
					

					# if noun_object.form in accepted_nouns:
					# 	freqs[(adverb_object.form, noun_object.form)] += 1
					# 	adverbs_freqs[adverb_object.form] += 1
					# 	nouns_freqs[noun_object.form] += 1
						# freqs[(determiner_object.form, adverb_object.form, noun_object.form)] += 1
	  					

				elif (
					next_object.pos == "ADJ" and \
					nnext_object.pos == "NOUN" and nnext_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == nnext_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == nnext_object.id)) 
				):                                                                          # DET ADV ADJ NOUN case
					
					noun_object = nnext_object
					adj_object = next_object
					ngramtype = "DET ADV ADJ NOUN"

					sentence_portion_right = sentence.sentence[c_id+3:min(len(sentence.sentence), c_id+3+ctx+1)]
					occurrence = sentence.sentence[c_id-1:c_id+3]


					# if noun_object.form in accepted_nouns:
					# 	freqs[(adverb_object.form, noun_object.form)] += 1
					# 	adverbs_freqs[adverb_object.form] += 1
					# 	nouns_freqs[noun_object.form] += 1
						# freqs[(determiner_object.form, adverb_object.form, adj_object.form, noun_object.form)] += 1
	  					


			if pprevious_object.pos == "DET":                                               # DET ? ADV ? case

				determiner_object = pprevious_object
				sentence_portion_left = sentence.sentence[max(0, c_id-2-ctx):c_id-2]

				if (
					previous_object.pos == "ADJ" and \
					next_object.pos == "NOUN" and next_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == next_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == next_object.id)) 
				):                                                                          # DET ADJ ADV NOUN case

					noun_object = next_object
					adj_object = previous_object
					ngramtype = "DET ADJ ADV NOUN"

					sentence_portion_right = sentence.sentence[c_id+2:min(len(sentence.sentence), c_id+1+ctx+1)]
					occurrence = sentence.sentence[c_id-2:c_id+2]
					
					
					# if noun_object.form in accepted_nouns:
					# 	freqs[(adverb_object.form, noun_object.form)] += 1
					# 	adverbs_freqs[adverb_object.form] += 1
					# 	nouns_freqs[noun_object.form] += 1
						# freqs[(determiner_object.form, adj_object.form, adverb_object.form, noun_object.form)] += 1

			if sentence_portion_left is not None and sentence_portion_right is not None:
				ctx_left = " ".join([token.form for token in sentence_portion_left])
				candidate_str = " ".join([token.form for token in occurrence])
				ctx_right = " ".join([token.form for token in sentence_portion_right])

				if not adverb_object.form in output_files:
					output_files[adverb_object.form] = open(f"../data/output/{adverb_object.form}.contexts.tsv", "w")

				print(f"{source}\t{adverb_object.form}\t{noun_object.form}\t{ngramtype}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=output_files[adverb_object.form])



	# with open(f"../data/output/{source}_{file_id}.ngrams.tsv", "w", encoding="utf-8") as fout:
	# 	for key, f in sorted(freqs.items(), key=lambda x: -x[1]):
	# 		if f > 0:
	# 			print(f"{f}\t{' '.join(key)}", file=fout)  

	# with open(f"../data/output/{source}_{file_id}.advs.tsv", "w", encoding="utf-8") as fout:
	# 	for key, f in sorted(adverbs_freqs.items(), key=lambda x: -x[1]):
	# 		if f > 0:
	# 			print(f"{f}\t{key}", file=fout)

	# with open(f"../data/output/{source}_{file_id}.nouns.tsv", "w", encoding="utf-8") as fout:
	# 	for key, f in sorted(nouns_freqs.items(), key=lambda x: -x[1]):
	# 		if f > 0:
	# 			print(f"{f}\t{key}", file=fout)              



if __name__ == "__main__":
	import utils

	# extract_NOUN("/home/ludovica/Documents/GitHub/new_TAM/data_sample/corpora/repubblica.1m", "REPUBBLICA", "01")

	accepted_nouns = utils.load_NOUNS("../data/output/REPUBBLICA_01.nouns.tsv", 0)
	accepted_prefs = utils.load_NOUNS("../data/output/REPUBBLICA_01.advs.tsv", 10)

	extract_ctx_detADVN("/home/ludovica/Documents/GitHub/new_TAM/data_sample/corpora/repubblica.1m", "REPUBBLICA", "01", accepted_nouns, accepted_prefs, 20, {})