import mysql.connector
import requests as re


#확장성 좋음 걍 리그 이름만 쭉 append 하면댐
tmpLeagueNameList = ["Premier League", "La Liga", "Bundesliga", "Ligue 1", "Serie A"]

headers={
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a68636f8f2c18511179c56f15e95080c"
}

hiddenLeagueId =[]

for i in range(len(tmpLeagueNameList)):
    getHiddenUrl = "https://v3.football.api-sports.io/leagues?name=%s" % tmpLeagueNameList[i]

    getHidden = re.get(url = getHiddenUrl, headers= headers)
    getHiddenRaw = getHidden.json()
    getHiddenData = getHiddenRaw['response']

    hiddenLeagueId.append(getHiddenData[0]['league']['id'])


print(hiddenLeagueId)
    

conn = mysql.connector.connect(user ='root', password='tmzkdnxj1', host='34.64.214.96', database ='scout', port = '3306')
cursor = conn.cursor()

for j in range(len(hiddenLeagueId)):
    insertHiddenSQL = 'insert into hidden_league_id (league_name, api_league_id) values ("%s", %d)' %(tmpLeagueNameList[j], hiddenLeagueId[j])
    cursor.execute(insertHiddenSQL)
    conn.commit()

conn.close()
