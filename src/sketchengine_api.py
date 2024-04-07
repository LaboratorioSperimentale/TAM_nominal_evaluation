# 2930da4e46236d168f3f7a783e0099e5

import requests
import re

USERNAME = 'ludovica.pannitto'
API_KEY = '2930da4e46236d168f3f7a783e0099e5'
base_url = 'https://api.sketchengine.eu/bonito/run.cgi'
data = {
 'corpname': 'preloaded/ittenten20_fl1',
 'ref_corpname': 'preloaded/ittenten20_fl1',
 'format': 'json',
 "wltype": "simple",
 "wlattr": "lempos_lc",
 "wlpat": "([a-z]+-)*[a-z][a-z]+(-[a-z]+)+-n",
 "wlsort": "frq",
 "wlmaxitems": 1000
}

d = requests.get(base_url + '/wordlist?corpname=%s' % data['corpname'], params=data, auth=(USERNAME, API_KEY)).json()
for el in d["Items"]:
	print(el)
	input()

# print("There are %d grammar relations for %s%s (lemma+PoS) in corpus %s." % (
#     len(d['Gramrels']), data['lemma'], data['lpos'], data['corpname']))