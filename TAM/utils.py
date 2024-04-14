import logging

import collections

import TAM.objects as objs
import TAM.pos_maps as pmaps


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/utils.log', format='%(levelname)s:%(message)s',
					encoding='utf-8', level=logging.DEBUG)

def read_wikiconll(fname):
	"""
	This Python function reads a file in the wikiCoNLL format and yields Sentence objects containing
	Token objects parsed from the file.

	Args:
	  fname: The `fname` parameter in the `read_wikiconll` function is a string that represents the file
	name or path to the file that contains the data in the wikiCoNLL format. This function reads the
	contents of the specified file, processes the data, and yields `Sentence` objects
	"""
	sentence = objs.Sentence(source="wikiCoNLL")

	with open(fname, encoding="utf-8") as fin:
		for line_n, line in enumerate(fin):
			line = line.strip()
			if line.startswith("<doc"):
				if not sentence.empty():
					yield sentence

				sentence = objs.Sentence(source="wikiCoNLL")

			elif len(line) == 0:
				if not sentence.empty():
					yield sentence

				sentence = objs.Sentence(source="wikiCoNLL")

			elif line.startswith("</doc"):
				pass

			else:
				line = line.strip().split("\t")

				tok_id = int(line[0])
				form = line[1]
				lemma = line[2]
				pos = line[3]
				head = -1
				deprel = ""
				try:
					head = int(line[6])
					deprel = line[7]
				except Exception as _:
					logger.info("Ignoring line %d", line_n)

				if pos in pmaps.wikiCoNLL_map:
					pos = pmaps.wikiCoNLL_map[pos]
				elif pos[0] in pmaps.wikiCoNLL_map:
					pos = pmaps.wikiCoNLL_map[pos[0]]

				token = objs.Token(tok_id, form, lemma, pos, head, deprel)
				sentence.add_token(token)
		if not sentence.empty():
			yield sentence


def read_repubblica(fname):
	"""
	This Python function reads a file containing data in a specific format from the "repubblica" source,
	parses the content, and yields sentences represented as objects with token information.

	Args:
	  fname: It looks like the code you provided is a Python function that reads a file in a specific
	format and yields sentences represented as objects. The function reads the file line by line,
	processes the lines, and creates tokens and sentences based on the content of the file.
	"""
	sentence = objs.Sentence(source="repubblica")

	with open(fname, encoding="utf-8") as fin:
		for line in fin:
			if line.startswith("<s"):
				if not sentence.empty():
					yield sentence

				sentence = objs.Sentence(source="repubblica")

			elif line.startswith("<"):
				pass

			else:
				line = line.strip().split("\t")

				tok_id = int(line[0])
				form = line[1].strip()
				lemma = line[2].strip()
				pos = line[4].strip()
				head = int(line[6])
				deprel = line[7].strip()

				if pos in pmaps.repubblica_map:
					pos = pmaps.repubblica_map[pos]
				elif pos[0] in pmaps.repubblica_map:
					pos = pmaps.repubblica_map[pos[0]]

				token = objs.Token(tok_id, form, lemma, pos, head, deprel)
				sentence.add_token(token)
		if not sentence.empty():
			yield sentence


def read_itwac(fname):
	"""
	The `read_itwac` function reads a file in the ITWAC format, parses the content to extract tokens and
	their attributes, and yields sentences containing the parsed tokens.

	Args:
	  fname: It looks like the code you provided is a Python function that reads a file in the ITWAC
	format and yields sentences. The function reads the file line by line, processes each line to
	extract token information, and creates a Sentence object with Token objects for each line of valid
	token data.
	"""

	sentence = objs.Sentence(source="itwac")

	with open(fname, encoding="iso-8859-1") as fin:

		for line_n, line in enumerate(fin):
			if line.startswith("<s"):
				if not sentence.empty():
					yield sentence

				sentence = objs.Sentence(source="itwac")
				start_id = 0

			elif line.startswith("<"):
				pass

			else:
				line = line.strip().split("\t")
				start_id += 1

				if len(line) == 3:

					tok_id = start_id
					form = line[0]
					lemma = line[2]
					pos = line[1].split(":")[0]
					if pos in pmaps.itwac_map:
						pos = pmaps.itwac_map[pos]

					token = objs.Token(tok_id, form, lemma, pos, -1, "")
					sentence.add_token(token)
				else:
					logger.info("Ignoring line %d", line_n)

		if not sentence.empty():
			yield sentence


def read(filename, source):
	"""
	The function `read` reads data from different sources based on the input `source` parameter.

	Args:
	  filename: The `filename` parameter in the `read` function is a string that represents the name or
	path of the file that you want to read data from.
	  source: The `source` parameter in the `read` function is used to determine from which specific
	source the data should be read. The function then calls different helper functions based on the
	value of the `source` parameter to read data from different sources such as "ITWAC", "REPUBBLICA

	Returns:
	  The function `read()` is returning the result of reading from the specified source based on the
	`source` parameter. The specific function being called and returned depends on the value of the
	`source` parameter.
	"""

	if source == "ITWAC":
		print("Reading from ITWAC")
		return read_itwac(filename)

	elif source == "REPUBBLICA":
		print("Reading from REPUBBLICA")
		return read_repubblica(filename)

	elif source == "WIKICONLL":
		print("Reading from WIKICONLL")
		return read_wikiconll(filename)
	else:
		logger.warning("Unable to read from source: %s", source)


def merge_frequencies(files_list, output_file):
	"""
	The function `merge_frequencies` reads data from multiple files, merges the frequencies of each
	unique key, and writes the merged frequencies to an output file.

	Args:
	  files_list: A list of file names that contain frequency data in the format of "count\tword" on
	each line. The function `merge_frequencies` reads these files and merges the frequencies of the same
	words into a single total frequency count.
	  output_file: The `output_file` parameter is a string that represents the file path where the
	merged frequencies will be written to. This function takes a list of file paths (`files_list`)
	containing frequency data and merges them into a single frequency count, which is then written to
	the specified `output_file`.
	"""

	total = collections.defaultdict(int)

	for filename in files_list:
		with open(filename, encoding="utf-8") as fin:
			for line in fin:
				linesplit = line.strip().split("\t")

				if len(linesplit) > 1:
					total[linesplit[1]] += int(linesplit[0])

	with open(output_file, "w", encoding="utf-8") as fout:
		for key, f in sorted(total.items()):
			print(f"{f}\t{key}", file=fout)


def load_from_file (input_filename, threshold):
	"""
	This Python function reads data from a file, filters it based on a threshold, and returns a set of
	accepted values.

	Args:
	  input_filename: The `input_filename` parameter is the name of the file from which the function
	`load_from_file` will read the data. This file should contain tab-separated values where the first
	value is an integer and the second value is a string.
	  threshold: The `threshold` parameter in the `load_from_file` function is used to filter out data
	based on a numerical value. In this case, the function reads a file where each line contains two
	values separated by a tab character. The function checks the first value (converted to an integer)
	against the threshold

	Returns:
	  The function `load_from_file` returns a set of strings that meet the specified threshold
	condition. The set contains the second element of each line in the input file where the first
	element is greater than or equal to the threshold value.
	"""
	accepted = set()

	with open(input_filename, encoding="utf-8") as fin:
		for line in fin:
			linesplit = line.strip().split("\t")
			f = int(linesplit[0])
			if f >= threshold:
				accepted.add(linesplit[1])

	return accepted


if __name__ == "__main__":
	for sentence in read_itwac("../data_sample/corpora/itwac.sample"):
		print(sentence)
		input()

	for sentence in read_repubblica("../data_sample/corpora/repubblica.sample"):
		print(sentence)
		input()

	for sentence in read_wikiconll("../data_sample/corpora/wikiconll.sample"):
		print(sentence)
		input()
