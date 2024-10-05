import requests

USERNAME = 'ludovica.pannitto'
API_KEY = '2930da4e46236d168f3f7a783e0099e5'
base_url = 'https://api.sketchengine.eu/bonito/run.cgi'
data = {
 'corpname': 'preloaded/ittenten20_fl1',
 'format': 'json',
 'wlattr': 'lempos',
 "wlpat": ".*-n",
 'wlminfreq': 0,
 "wlmaxitems": 10000000,

}
d = requests.get(base_url + '/wordlist?corpname=%s' % data['corpname'], params=data, auth=(USERNAME, API_KEY)).json()
print(d)

