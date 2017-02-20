import requests
import json

r = requests.get('https://intra.epitech.eu/', data = {'format':'json','login':'','password':''})
print r.content