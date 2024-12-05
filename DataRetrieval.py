import json
import urllib.request

def getCardData():
    f = open('txt/Key.txt', 'r')
    key = f.read().strip('\n').strip('')

    url = 'https://api.clashroyale.com/v1'
    endpoint = '/cards'

    request = urllib.request.Request(
        url + endpoint,
        None,
        headers={
            'Accept': 'application/json',
            'authorization': f'Bearer {key}'
        }
    )

    response = urllib.request.urlopen(request).read().decode('utf-8')
    Data = json.loads(response)
    cardData = Data['items']
    towerData = Data['supportItems']

def getPlayerData(playerTag):
    f = open('txt/Key.txt', 'r')
    key = f.read().strip('\n').strip('')

    playerTag = '%23' + playerTag[1:]

    url = 'https://api.clashroyale.com/v1'
    endpoint = f'/players/{playerTag}'

    request = urllib.request.Request(
        url + endpoint,
        None,
        headers={
            'Accept': 'application/json',
            'authorization': f'Bearer {key}'
        }
    )

    response = urllib.request.urlopen(request).read().decode('utf-8')
    Data = json.loads(response)
    return(Data)
    
def getCurrentSeason():
    f = open('txt/Key.txt', 'r')
    key = f.read().strip('\n').strip('')

    url = 'https://api.clashroyale.com/v1'
    endpoint = '/locations/global/seasons'

    request = urllib.request.Request(
        url + endpoint,
        None,
        headers={
            'Accept': 'application/json',
            'authorization': f'Bearer {key}'
        }
    )

    response = urllib.request.urlopen(request).read().decode('utf-8')
    Data = json.loads(response)
    return Data['items'][-1]['id']


def getTopPlayers():
    f = open('txt/Key.txt', 'r')
    key = f.read().strip('\n').strip('')

    seasonId = getCurrentSeason()

    url = 'https://api.clashroyale.com/v1'
    endpoint = f'/locations/global/pathoflegend/{seasonId}/rankings/players'

    request = urllib.request.Request(
        url + endpoint,
        None,
        headers={
            'Accept': 'application/json',
            'authorization': f'Bearer {key}'
        }
    )

    response = urllib.request.urlopen(request).read().decode('utf-8')
    Data = json.loads(response)
    players = Data['items']
    return(players)
    
def getTopDecks():

    topPlayers = getTopPlayers()[:1000]
    decks = []
    f = open('txt/topPlayers.txt', 'a', encoding="utf-8")
    bannedPlayers = []
    i = 0
    for topPlayer in topPlayers:
        try:
            decks.append({'name': topPlayer['name'], 'tag': topPlayer['tag'], 'deck': getPlayerData(topPlayer['tag'])['currentDeck']})
            print(i)
        except:
            bannedPlayers.append(topPlayer['tag'])
            pass
        i += 1

    jsonDecks = json.dumps(decks)
    jsonBannedPlayers = json.dumps(bannedPlayers)
    f.write(jsonDecks)
    f = open('txt/bannedPlayers.txt', 'a', encoding="utf-8")
    f.write(jsonBannedPlayers)

def getBattleLog(playerTag):

    playerTag = '%23' + playerTag[1:]

    f = open('txt/Key.txt', 'r')
    key = f.read().strip('\n').strip('')

    seasonId = getCurrentSeason()

    url = 'https://api.clashroyale.com/v1'
    endpoint = f'/players/{playerTag}/battlelog'

    request  = urllib.request.Request(
        url + endpoint,
        None,
        headers={
            'Accept': 'application/json',
            'authorization': f'Bearer {key}'
        }
    )

    response = urllib.request.urlopen(request).read().decode('utf-8')
    Data = json.loads(response.replace('\'',""))
    f = open('txt/battleLog.txt', 'r', encoding="utf-8")
    s = f.read()
    f = open('txt/battleLog.txt', 'a', encoding="utf-8")
    for battle in Data:
        if battle['battleTime'] not in s:
            f.write(str(battle) + ",")
            
    
    f = open('txt/battleLog.txt', 'r', encoding="utf-8")
    Data = '[' + f.read()[:len(f.read())-1].replace('\'','"') + ']'
    Data = Data.replace('False','false').replace('None','null').replace('True','true')
    return(json.loads(Data))

