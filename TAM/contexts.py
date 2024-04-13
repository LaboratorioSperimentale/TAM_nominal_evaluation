import tqdm

import TAM.utils as utils


def extract_ctx_advN(filename, source,
					 accepted_prefs, accepted_nouns,
					 ctx,
					 output_dir, output_files):
	"""
	This Python function extracts context for prefix-noun compounds from a given file based on specified
	criteria and writes the results to output files.

	Args:
	  filename: The `filename` parameter in the `extract_ctx_advN` function is the name of the file from
	which the sentences will be read for processing.
	  source: The `source` parameter in the `extract_ctx_detADVN` function is a string
	representing the source of the data from which you are extracting contexts for compounds.
	  accepted_prefs: The `accepted_prefs` parameter in the `extract_ctx_advN` function is a set that
	contains accepted prefixes. These are prefixes that are considered valid or allowed for extraction
	in the context of the function's operation.
	  accepted_nouns: Accepted_nouns is a list of accepted noun forms that the function will use to
	filter out nouns in the input data.
	  ctx: The `ctx` parameter in the `extract_ctx_advN` function represents the context window size. It
	determines how many tokens to consider on the left and right of a candidate noun in a sentence when
	extracting context information. The context window size `ctx` specifies the number of tokens before
	and after the compound
	  output_dir: The `output_dir` parameter in the `extract_ctx_advN` function represents the directory
	where the output files will be saved. It is a path to the directory where the generated context
	files will be stored.
	  output_files: The `output_files` parameter in the `extract_ctx_advN` function is a dictionary that
	stores file objects for writing the extracted context information. The keys in the dictionary are
	prefixes, and the values are file objects associated with those prefixes. Each file object is opened
	for writing in UTF-8 encoding
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
				output_files[prefix] = open(output_dir.joinpath(f"{prefix}.contexts.tsv"),
								"w", encoding="utf-8")

			print(f"{source}\t{prefix}\t{noun}\t{ctx_left}\t{candidate_str}\t{ctx_right}",
		 		file=output_files[prefix])


def extract_ctx_detADVN(filename, source,
						accepted_adverbs, accepted_nouns,
						ctx,
						output_dir, output_files):
	"""
	The function `extract_ctx_detADVN` takes in a filename, source, accepted nouns, accepted adverbs,
	context, output directory, and output files. It processes sentences to extract specific patterns
	involving adverbs, nouns, and determiners, and writes the extracted information to output files.

	Args:
	  filename: The `filename` parameter in the `extract_ctx_detADVN` function is the name of the file
	from which the sentences will be read for processing.
	  source: The `source` parameter in the `extract_ctx_detADVN` function is a string
	representing the source of the data from which you are extracting contexts for adverbs and nouns.
	  accepted_nouns: Accepted_nouns is a list of accepted noun forms that the function will use to
	filter out nouns in the input data.
	  accepted_adverbs: The `accepted_adverbs` parameter in the `extract_ctx_detADVN` function is a list
	of adverbs that are considered acceptable for extraction. These adverbs are used to filter out
	adverbs that are not of interest for the extraction process.
	  ctx: The `ctx` parameter in the `extract_ctx_detADVN` function represents the context size, which
	determines how many tokens to consider on the left and right sides of the adverb in a sentence when
	extracting information. It is used to define the window size for capturing the surrounding context
	of the adverb-noun pattern
	  output_dir: The `output_dir` parameter in the `extract_ctx_detADVN` function represents the
	directory where the output files will be saved. It is a path to the directory where the output files
	containing the extracted contexts will be stored.
	  output_files: The `output_files` parameter in the `extract_ctx_detADVN` function is a dictionary
	that stores file objects for writing output data. The keys in the dictionary are the adverb forms,
	and the values are the corresponding file objects where the extracted context information will be
	written. Each file object is opened for writing in UTF-8 encoding
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

			pprevious_object = sentence.sentence[c_id-2]
			previous_object = sentence.sentence[c_id-1]

			next_object = sentence.sentence[c_id+1]
			nnext_object = sentence.sentence[c_id+2]

			if previous_object.pos == "DET":                                            # DET ADV ? ? case

				sentence_portion_left = sentence.sentence[max(0, c_id-1-ctx):c_id-1]

				determiner_object = previous_object

				if (
					next_object.pos == "NOUN" and next_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == adverb_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == next_object.id))
				):                                                                      # DET ADV NOUN case

					noun_object = next_object
					ngramtype = "DET ADV NOUN"

					sentence_portion_right = sentence.sentence[c_id+2:min(len(sentence.sentence), c_id+2+ctx+1)]
					occurrence = sentence.sentence[c_id-1:c_id+2]

				elif (
					next_object.pos == "ADV" and \
					nnext_object.pos == "NOUN" and nnext_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == nnext_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == nnext_object.id) or \
					(next_object.deprel == "" or next_object.head == nnext_object.id))
				):                                                                      # DET ADV ADV NOUN case

					noun_object = nnext_object
					adverb_object.form = adverb_object.form + " " + next_object.form
					ngramtype = "DET ADV NOUN"
					sentence_portion_right = sentence.sentence[c_id+3:min(len(sentence.sentence), c_id+3+ctx+1)]
					occurrence = sentence.sentence[c_id-1:c_id+3]

				elif (
					next_object.pos == "ADJ" and \
					nnext_object.pos == "NOUN" and nnext_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == nnext_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == nnext_object.id))
				):                                                                      # DET ADV ADJ NOUN case

					noun_object = nnext_object
					# adj_object = next_object
					ngramtype = "DET ADV ADJ NOUN"

					sentence_portion_right = sentence.sentence[c_id+3:min(len(sentence.sentence), c_id+3+ctx+1)]
					occurrence = sentence.sentence[c_id-1:c_id+3]


			if pprevious_object.pos == "DET":                                           # DET ? ADV ? case

				determiner_object = pprevious_object
				sentence_portion_left = sentence.sentence[max(0, c_id-2-ctx):c_id-2]

				if (
					previous_object.pos == "ADJ" and \
					next_object.pos == "NOUN" and next_object.form in accepted_nouns and \
					((determiner_object.deprel == "" or determiner_object.head == next_object.id) or \
					(adverb_object.deprel == "" or adverb_object.head == next_object.id))
				):                                                                      # DET ADJ ADV NOUN case

					noun_object = next_object
					# adj_object = previous_object
					ngramtype = "DET ADJ ADV NOUN"

					sentence_portion_right = sentence.sentence[c_id+2:min(len(sentence.sentence), c_id+1+ctx+1)]
					occurrence = sentence.sentence[c_id-2:c_id+2]


			if sentence_portion_left is not None and sentence_portion_right is not None:
				ctx_left = " ".join([token.form for token in sentence_portion_left])
				candidate_str = " ".join([token.form for token in occurrence])
				ctx_right = " ".join([token.form for token in sentence_portion_right])

				if not adverb_object.form in output_files:
					output_files[adverb_object.form] = open(output_dir.joinpath(f"{adverb_object.form}.contexts.tsv"),
															"w",
															encoding="utf-8")

				print(f"{source}\t{adverb_object.form}\t{noun_object.form}\t" \
		  			f"{ngramtype}\t{ctx_left}\t{candidate_str}\t{ctx_right}",
		  			file=output_files[adverb_object.form])
