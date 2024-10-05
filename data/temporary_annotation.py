import pathlib
import os

import tqdm

nouns_map = {}
for line in open("nomi.sorted"):
	line = line.strip().split("\t")
	nouns_map[line[0]] = line[1]




for filename in tqdm.tqdm(pathlib.Path("ngrams_samples").glob("*sampled*")):
	os.rename(filename, f"{filename}.bak")

	with open(f"{filename}.bak") as fin, \
	open(filename, "w") as fout:

		for line in fin:

			source, pref, noun, *rest = line.strip().split("\t")

			noun_label = "?"
			if noun in nouns_map:
				noun_label = nouns_map[noun]

			rest_str = '\t'.join(rest)
			print(f"{source}\t{pref}\t{noun}\t{noun_label}\t?\t{rest_str}", file=fout)
			# print(line.strip().split("\t"))
			# input()