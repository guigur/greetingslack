import websocket
import json
import requests
import urllib
import os


# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
	MESSAGE = os.environ['WELCOME-MESSAGE'] 
	TOKEN = os.environ['SLACK-TOKEN']
except:
	MESSAGE = 'salut'
	TOKEN = 'le tocken'
###############################################################

def parse_join(message):
    m = json.loads(message)
    if (m['type'] == "message"):
        
        k = requests.get("https://slack.com/api/users.info?token="+TOKEN+"&user="+m["user"])
        k = k.json()
        print  '\033[92m' + k['user']['profile']['email'] + '\033[0m'
        requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel=mmmmm&text="+urllib.quote("lol")+"&parse=full&as_user=true")


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


if __name__ == "__main__":
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    #ws.on_open
    ws.run_forever()
