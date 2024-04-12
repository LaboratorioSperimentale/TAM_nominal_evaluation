import tqdm

import TAM.utils as utils

def extract_ctx_advN(filename, source, file_id, accepted_prefs, accepted_nouns, ctx, output_files):
	"""
	This Python function extracts compound nouns from a given file, identifies relevant prefixes and
	nouns based on specified criteria, and outputs the context surrounding each compound noun occurrence
	to separate files based on prefixes.

	Args:
	  filename: The `filename` parameter in the function `extract_ctx_advN` is the name of the file from
	which you are reading the data.
	  source: The `source` parameter in the function `extract_ctx_advN` is typically used to specify the
	source of the data or text that is being processed. It could be a file path, a data source
	identifier, or any other information that helps identify where the input data is coming from.
	  file_id: The `file_id` parameter in the `extract_ctx_advN` function seems to be unused in the
	provided code snippet. It is defined as a parameter but not utilized within the function. If you
	intended to use it for some specific purpose, you may need to update the function implementation to
	incorporate the
	  accepted_prefs: Accepted prefixes for compound nouns
	  accepted_nouns: The `accepted_nouns` parameter in the `extract_ctx_advN` function is a list of
	nouns that are considered acceptable for extraction. These nouns are filtered based on certain
	criteria within the function to determine which ones should be included in the output.
	  ctx: The `ctx` parameter in the `extract_ctx_advN` function represents the context size, which
	determines how many tokens to consider on the left and right of a candidate noun in a sentence. It
	is used to extract the context surrounding a candidate noun in a text. The value of `ctx`
	  output_files: The `output_files` parameter is a dictionary that stores file objects for writing
	output data. The keys in the dictionary are prefixes, and the values are file objects opened for
	writing the output data related to that prefix. The function opens a new file for each unique prefix
	in the `output_files` dictionary
	"""

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
				output_files[prefix] = open(f"../data/output/{prefix}.contexts.tsv", "w", encoding="utf-8")

			print(f"{source}\t{prefix}\t{noun}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=output_files[prefix])


def extract_ctx_detADVN(filename, source, file_id, accepted_nouns, accepted_adverbs, ctx, output_files):
	"""
	The function `extract_ctx_detADVN` reads a file, extracts specific adverbs and their surrounding
	context in sentences, and writes the extracted information to output files based on certain
	conditions.

	Args:
	  filename: The `filename` parameter in the `extract_ctx_detADVN` function is the name of the file
	from which sentences will be read for processing.
	  source: The `source` parameter in the `extract_ctx_detADVN` function is typically used to specify
	the source of the data or text that is being processed. It could be a file path, a data source
	identifier, or any other information that helps identify where the input data is coming from.
	  file_id: The `file_id` parameter in the `extract_ctx_detADVN` function seems to be missing from
	the provided code snippet. Could you please provide more information or context about the `file_id`
	parameter so that I can assist you further with its usage in the function?
	  accepted_nouns: Accepted_nouns is a list of nouns that have been deemed acceptable for extraction
	in the provided function. These nouns are likely relevant to the context in which they appear and
	are specified as criteria for selecting certain instances during the extraction process.
	  accepted_adverbs: The function `extract_ctx_detADVN` takes several parameters including
	`filename`, `source`, `file_id`, `accepted_nouns`, `accepted_adverbs`, `ctx`, and `output_files`.
	  ctx: The `ctx` parameter in the `extract_ctx_detADVN` function represents the context size, which
	determines how many tokens to consider on the left and right sides of the adverb in a sentence when
	extracting information. It is used to define the window size for capturing surrounding tokens for
	analysis.
	  output_files: The `output_files` parameter in the `extract_ctx_detADVN` function is a dictionary
	that stores file objects for writing output data. The keys in the dictionary are the adverbs
	extracted from the input data, and the values are file objects opened for writing the extracted
	contexts.
	"""


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
					output_files[adverb_object.form] = open(f"../data/output/{adverb_object.form}.contexts.tsv",
											 "w",
											 encoding="utf-8")

				print(f"{source}\t{adverb_object.form}\t{noun_object.form}\t{ngramtype}\t{ctx_left}\t{candidate_str}\t{ctx_right}", file=output_files[adverb_object.form])



if __name__ == "__main__":

	accepted_nouns = utils.load_NOUNS("../data/output/REPUBBLICA_01.nouns.tsv", 0)
	accepted_prefs = utils.load_NOUNS("../data/output/REPUBBLICA_01.advs.tsv", 10)

	extract_ctx_detADVN("/home/ludovica/Documents/GitHub/new_TAM/data_sample/corpora/repubblica.1m",
					 "REPUBBLICA", "01", accepted_nouns, accepted_prefs, 20, {})
