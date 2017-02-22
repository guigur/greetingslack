import requests
import json
import Cookie
import ConfigParser


def epiLogin():
    Config = ConfigParser.ConfigParser()
    Config.read("config.txt")
    login = Config.get('Epitech', 'login')
    password = Config.get('Epitech', 'password')
    
    s = requests.Session()
    splittedemail = login.split('@')

    if splittedemail[1] == 'epitech.eu':
        auth = s.post('https://intra.epitech.eu/', data = {'format':'json','login':login,'password':password, 'remember_me':'on'})
        try:
            json_line = json.loads(auth.content)
        except ValueError:
            getInfo(s)
        else:
            auth = auth.json()
            print "Can't conenct to the epitech intranet: " + auth['message']


def getInfo(s):
    loginToGetInfos = "guillaume.arthaud@epitech.eu"
    r = s.post('https://intra.epitech.eu/user/'+loginToGetInfos+'?format=json')
    r = r.json()
    print r['groups']
	
epiLogin()