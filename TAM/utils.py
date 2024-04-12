import logging

import collections

import TAM.objects as objs
import TAM.pos_maps as pmaps


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/utils.log', format='%(levelname)s:%(message)s', 
					encoding='utf-8', level=logging.DEBUG)

def read_wikiconll(fname):
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
				# print(line)

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

	total = collections.defaultdict(int)

	for filename in files_list:
		with open(filename) as fin:
			for line in fin:
				linesplit = line.strip().split("\t")

				total[linesplit[1]] += int(linesplit[0])

	with open(output_file, "w", encoding="utf-8") as fout:
		for key, f in sorted(total.items()):
			print(f"{f}\t{key}", file=fout)



def load_NOUNS (input_filename, threshold):
	accepted = set()

	with open(input_filename) as fin:
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