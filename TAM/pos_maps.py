"""
This python module contains maps in the form of dictionaries. These allow to have a uniform
denomination for part of speech tags for data coming from different sources.
"""
itwac_map = {
             "ADJ": "ADJ",
             "ADV": "ADV",
			 "NEG": "ADV",
             "ART": "DET",
             "ARTPRE": "DET",
			 "DET:demo": "DET",
			 "DET:indef": "DET",
			 "DET:num": "DET",
			 "DET:poss": "DET",
			 "DET:wh": "DET",
			 "NOUN": "NOUN",
			 "DET": "X"}

repubblica_map = {
             "A": "ADJ",
             "EA": "DET",
             "DD": "DET",
             "DI": "DET",
             "DE": "DET",
             "DQ": "DET",
             "DR": "DET",
             "B": "ADV",
             "R": "DET",
             "S": "NOUN",
            }

wikiCoNLL_map = {
    "S": "NOUN",
    "R": "DET",
    "EA": "DET",
    "A": "ADJ",
    "B": "ADV",
    "D": "DET",
}