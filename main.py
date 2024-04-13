import argparse
import pathlib
from pathlib import Path

import tqdm

import TAM.extract as e
import TAM.contexts as c
import TAM.utils as u


def _compute_noun_frequencies(args):
	"""
	The function `_compute_noun_frequencies` reads a list of input files, processes each file to extract
	nouns, and saves the results in an output directory.

	Args:
	  args: It looks like the function `_compute_noun_frequencies` takes in a single argument `args`.
	This argument likely contains information such as a configuration file path, a list of input files,
	and an output folder path. The function reads a list of input files from a file specified in
	`args.input
	"""
	# stream = open(args.conf_file)
	# dictionary = yaml.load(stream, Loader)

	input_files = []
	with open(Path(args.input_files_list), encoding="utf-8") as fin:
		for line in fin:
			linesplit = line.strip().split("\t")
			source, file_id, path = linesplit
			path = Path(path)
			input_files.append((source, file_id, path))

	output_directory = Path(args.output_folder)
	output_directory.mkdir(parents=True, exist_ok=True)

	for source, file_id, path in tqdm.tqdm(input_files):
		e.extract_NOUN(path, source, file_id, output_directory)


def _merge_frequencies(args):
	"""
	The function `_merge_frequencies` takes input filenames matching a specific pattern, merges their
	frequencies, and saves the result to an output file.

	Args:
	  args: It looks like the code snippet you provided is calling a function `_merge_frequencies` with
	the `args` parameter. The `args` parameter seems to be an object or dictionary containing the
	following attributes:
	"""
	# stream = open(args.conf_file)
	# dictionary = yaml.load(stream, Loader)

	input_filenames = Path(args.input_folder).glob(f"*{args.pattern}*")
	output_filename = Path(args.output_folder).joinpath(f"{args.output_filename}")

	u.merge_frequencies(input_filenames, output_filename)


def _extract_raw(args):
	"""
	The function `_extract_raw` reads input files, creates output directories, loads accepted nouns, and
	extracts information based on the specified type.

	Args:
	  args: The code snippet you provided seems to be a part of a script that extracts information from
	input files based on certain criteria and saves the output in a specified directory. The script uses
	various functions like `load_NOUNS`, `extract_advN`, and `extract_detADVN` to process the input
	"""
	# stream = open(args.conf_file)
	# dictionary = yaml.load(stream, Loader)

	input_files = []
	with open(Path(args.input_files), encoding="utf-8") as fin:
		for line in fin:
			linesplit = line.strip().split("\t")
			source, file_id, path = linesplit
			path = Path(path)
			input_files.append((source, file_id, path))

	output_directory = Path(args.output_folder)
	output_directory.mkdir(parents=True, exist_ok=True)

	accepted_nouns = u.load_from_file(args.nouns_filename, args.threshold)

	for source, file_id, path in tqdm.tqdm(input_files):
		if args.type == "compound":
			e.extract_advN(path, source, file_id, accepted_nouns, output_directory)
		elif args.type == "ngram":
			e.extract_detADVN(path, source, file_id, accepted_nouns, output_directory)

def _extract_contexts(args):
	input_files = []
	with open(Path(args.input_files), encoding="utf-8") as fin:
		for line in fin:
			linesplit = line.strip().split("\t")
			source, file_id, path = linesplit
			path = Path(path)
			input_files.append((source, file_id, path))

	output_directory = Path(args.output_folder)
	output_directory.mkdir(parents=True, exist_ok=True)

	if args.type == "compound":
		accepted_nouns = u.load_from_file(args.accepted_nouns, args.nouns_threshold)
		accepted_prefs = u.load_from_file(args.accepted_prefs, args.prefs_threshold)
	elif args.type == "ngram":
		accepted_nouns = u.load_from_file(args.accepted_nouns, args.nouns_threshold)
		accepted_adverbs = u.load_from_file(args.accepted_adverbs, args.adverbs_threshold)


	output_files = {}
	for source, file_id, path in tqdm.tqdm(input_files):
		if args.type == "compound":
			c.extract_ctx_advN(path, source,
					  accepted_prefs, accepted_nouns,
					  args.context_width, output_directory, output_files)
		elif args.type == "ngram":
			c.extract_ctx_detADVN(path, source,
						 accepted_adverbs, accepted_nouns,
						 args.context_width, output_directory, output_files)


def _filter(args):
	pass

if __name__ == "__main__":

	parent_parser = argparse.ArgumentParser(add_help=False)

	root_parser = argparse.ArgumentParser(prog='TAM', add_help=True)
	subparsers = root_parser.add_subparsers(title="actions", dest="actions")


	parser_frequencies = subparsers.add_parser('frequencies', parents=[parent_parser],
											   description='compute frequency of NOUNS',
											   help='compute frequency of NOUNS')
	# parser_frequencies.add_argument("-c", "--conf-file", default="cfg/conf.yml",
	# 							   help="path to yaml configuration file")
	parser_frequencies.add_argument("-i", "--input-files-list", default="data_sample/files_input.tsv",
								 type=pathlib.Path,
								 help="path to file containing list of input files")
	parser_frequencies.add_argument("-o", "--output-folder", default="data_sample/output_frequencies/",
								 type=pathlib.Path,
								 help="path to output folder")
	parser_frequencies.set_defaults(func=_compute_noun_frequencies)


	parser_merge = subparsers.add_parser("merge", parents=[parent_parser],
										description='merge frequency lists',
										help='merge frequency lists')
	# parser_merge.add_argument("-c", "--conf-file", default="cfg/conf.yml",
	# 						  help="path to yaml configuration file")
	parser_merge.add_argument("-i", "--input-folder", default="data_sample/output_frequencies",
						   type=pathlib.Path,
						   	 help="path to folder containing files to merge")
	parser_merge.add_argument("-p", "--pattern", default="NOUNS",
						   type=str,
						   help="pattern of filenames to be merged")
	parser_merge.add_argument("-o", "--output-folder", default="data_sample/output_frequencies",
						   type=pathlib.Path,
						   help="path to output folder")
	parser_merge.add_argument("--output-filename", default="accepted.tsv",
						   type=str,
						   help="name for merged file")
	parser_merge.set_defaults(func=_merge_frequencies)


	parser_extract = subparsers.add_parser("extract", parents=[parent_parser],
											description='extract raw data',
											help='extract raw data')
	parser_extract.add_argument("-i", "--input-files-list", default="data_sample/files_input.tsv",
							 type=pathlib.Path,
							 help="path to file containing list of input files")
	parser_extract.add_argument("--type", choices=["compound", "ngram"], default="compound",
							    help="type of structures to extract")
	parser_extract.add_argument("-o", "--output-folder",
							 type=pathlib.Path,
							 default="data_sample/output_compoundfrequencies/",
							 help="path to output folder")
	parser_extract.add_argument("--accepted-nouns",
							 default="data_sample/output_frequencies/accepted.tsv",
							 type=pathlib.Path,
							 help="path to list of accepted nouns")
	parser_extract.add_argument("-t", "--threshold", default=10, type=int,
							 help="minimum noun frequency")
	parser_extract.set_defaults(func=_extract_raw)


	parser_contexts = subparsers.add_parser("contexts", parents=[parent_parser],
											description='extract contexts',
											help='contexts')
	parser_contexts.add_argument("-i", "--input-files", default="data_sample/files_input.tsv",
							  type=pathlib.Path,
							  help="path to file containing list of input files")
	parser_contexts.add_argument("--type", choices=["compound", "ngram"], default="compound",
							    help="type of structures to extract")
	parser_contexts.add_argument("-o", "--output-folder",
							  type=pathlib.Path,
							  default="data_sample/output_compoundfrequencies/",
							  help="path to output folder")
	parser_contexts.add_argument("--accepted-nouns", default="data_sample/final_lists/nouns.txt",
							  type=pathlib.Path,
							  help="path to list of accepted nouns")
	parser_contexts.add_argument("--accepted-prefs", default="data_sample/final_lists/prefixes.txt",
							  type=pathlib.Path,
							  help="path to list of accepted prefixes")
	parser_contexts.add_argument("--accepted-adverbs", default="data_sample/final_lists/adverbs.txt",
							  type=pathlib.Path,
							  help="path to list of accepted adverbs")
	parser_contexts.add_argument("--nouns-threshold", type=int, default=20,
							  help="minimum noun frequency")
	parser_contexts.add_argument("--adverbs-threshold", type=int, default=20,
							  help="minimum adverb frequency")
	parser_contexts.add_argument("--prefs-threshold", type=int, default=20,
							  help="minimum prefix frequency")
	parser_contexts.add_argument("-c", "--context-width", type=int, default=20,
							     help="width of left and right sentence context")
	parser_contexts.set_defaults(func=_extract_contexts)

	args = root_parser.parse_args()

	if "func" not in args:
		root_parser.print_usage()
		exit()

	args.func(args)
