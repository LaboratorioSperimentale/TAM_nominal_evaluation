import tqdm
import yaml
try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader
	

import argparse
from pathlib import Path


import TAM.extract as e
import TAM.utils as u



def _compute_noun_frequencies(args):
	stream = open(args.conf_file)
	dictionary = yaml.load(stream, Loader)
	
	input_files = []
	with open(Path(dictionary["input_files"])) as fin:
		for line in fin:
			linesplit = line.strip().split("\t")
			source, file_id, path = linesplit
			path = Path(path)
			input_files.append((source, file_id, path))

	output_directory = Path(dictionary["output_folder"])
	output_directory.mkdir(parents=True, exist_ok=True)

	for source, file_id, path in tqdm.tqdm(input_files):
		e.extract_NOUN(path, source, file_id, output_directory)


def _merge_frequencies(args):
	stream = open(args.conf_file)
	dictionary = yaml.load(stream, Loader)

	input_filenames = Path(dictionary["input_folder"]).glob("*NOUNS*")
	output_filename = Path(dictionary["output_folder"]).joinpath("accepted.tsv")

	u.merge_frequencies(input_filenames, output_filename)


if __name__ == "__main__":

	parent_parser = argparse.ArgumentParser(add_help=False)

	root_parser = argparse.ArgumentParser(prog='TAM', add_help=True)
	subparsers = root_parser.add_subparsers(title="actions", dest="actions")


	parser_frequencies = subparsers.add_parser('frequencies', parents=[parent_parser],
											   description='compute frequency of NOUNS',
											   help='compute frequency of NOUNS')
	parser_frequencies.add_argument("-c", "--conf-file", default="cfg/conf.yml",
								   help="path to yaml configuration file")
	parser_frequencies.set_defaults(func=_compute_noun_frequencies)


	parser_merge = subparsers.add_parser("merge", parents=[parent_parser],
										description='merge frequency lists',
										help='merge frequency lists')
	parser_merge.add_argument("-c", "--conf-file", default="cfg/conf.yml",
							  help="path to yaml configuration file")
	parser_merge.set_defaults(func=_merge_frequencies)

	args = root_parser.parse_args()

	if "func" not in args:
		root_parser.print_usage()
		exit()

	args.func(args)