import requests
import mysql.connector
import requests as re

tmpLeagueIdList = []
hiddenTeamId =[]

currentSeason = 2022

conn = mysql.connector.connect(user ='root', password='tmzkdnxj1', host='34.64.214.96', database ='scout', port = '3306')
cursor = conn.cursor()

getLeagueIdSQL = 'select api_league_id from hidden_league_id'
getLeagueIdRaw = cursor.execute(getLeagueIdSQL)
hiddenLeagueIdRaw = cursor.fetchall()

for i in range(len(hiddenLeagueIdRaw)):
    tmpLeagueIdList.append(hiddenLeagueIdRaw[i][0])


print(tmpLeagueIdList)


headers={
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a68636f8f2c18511179c56f15e95080c"
}


for j in range(len(tmpLeagueIdList)):
    getHiddenUrl = "https://v3.football.api-sports.io/teams?league=%s&season=%d" %(tmpLeagueIdList[j], currentSeason)
    #print(getHiddenUrl)

    tmpTeamIdRaw = re.get(url = getHiddenUrl, headers = headers).json()
    tmpTeamIdData = tmpTeamIdRaw['response']
    tmpTeamCount = tmpTeamIdRaw['results']
    
    for k in range(tmpTeamCount):
        tmpBlock = []
        tmpBlock.append(tmpTeamIdData[k]['team']['id'])
        tmpBlock.append(tmpTeamIdData[k]['team']['name'])
        hiddenTeamId.append(tmpBlock)

print(hiddenTeamId)
print(type(hiddenTeamId[0][1]))


for i in range(len(hiddenTeamId)):
    injectionSQL = 'insert into hidden_team_id (api_team_id, team_name) values (%d, "%s")' %(hiddenTeamId[i][0], hiddenTeamId[i][1])
    cursor.execute(injectionSQL)
    conn.commit()

conn.close()



