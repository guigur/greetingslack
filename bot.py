import websocket
import json
import requests
import Cookie
import ConfigParser
import urllib
import os
import logging

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
    TOKEN = os.environ['SLACK-TOKEN']
    CHANNEL = os.environ['SLACK-CHANNEL']
except:
    TOKEN = 'token'
    CHANNEL = 'general'

###############################################################
def epiLogin(loginToGetInfos):
    totgroup = ""
    Config = ConfigParser.ConfigParser()
    Config.read("config.txt")
    login = Config.get('Epitech', 'login')
    password = Config.get('Epitech', 'password')
    s = requests.Session()
    auth = s.post('https://intra.epitech.eu/', data = {'format':'json','login':login,'password':password, 'remember_me':'on'})
    infos = getInfo(s, loginToGetInfos)
    groups = infos['groups']
    for group in groups:
        if totgroup != "":
            totgroup = totgroup + ", "
        totgroup = totgroup + group['title']
    print totgroup
    message = "Bienvenue " + infos['title'].title() + "\r" + "https://intra.epitech.eu/user/" + urllib.quote(loginToGetInfos) + "\rpromo : " + str(infos['promo']) + "\rgroupes :  " + totgroup
    requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+CHANNEL+"&text="+message+"&parse=full&as_user=true")

def getInfo(s, loginToGetInfos):
    r = s.post('https://intra.epitech.eu/user/'+loginToGetInfos+'?format=json')
    print r.content
    r = r.json()
    return r
	
def parse_join(message):
    m = json.loads(message)
    if (m['type'] == "message"):   
        k = requests.get("https://slack.com/api/users.info?token="+TOKEN+"&user="+m["user"])
        k = k.json()
        loginToGetInfos = k['user']['profile']['email']
        print  '\033[92m' + loginToGetInfos + '\033[0m'
        splittedemail = loginToGetInfos.split('@')
        if splittedemail[1] == 'epitech.eu':
            epiLogin(loginToGetInfos)

#Connects to Slacks and initiates socket handshake        
def start_rtm():
    print "https://slack.com/api/rtm.start?token=" + TOKEN
    r = requests.get("https://slack.com/api/rtm.start?token="+TOKEN, verify=False)
    r = r.json()
    r = r["url"]
    return r

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    print "SOME ERROR HAS HAPPENED", error

def on_close(ws):
    print '\033[91m'+"Connection Closed"+'\033[0m'

def on_open(ws):
    print "Connection Started - Auto Greeting new joiners to the network"

logging.basicConfig()
r = start_rtm()
ws = websocket.WebSocketApp(r, on_message = on_message)
#ws.on_open
ws.run_forever()
