import requests
import mysql.connector
import requests as re

#PL 스크립트에서 필요한 상수값 + 확장성은 hidden에서 끌어올수 있음 좋음
tmpLeagueName = "Premier League"
tmpSeasonYear = 2022
tmpLeagueID = 39

getTeamUrl = "https://v3.football.api-sports.io/teams?season=%d&league=%d" %(tmpSeasonYear, tmpLeagueID)
headers={
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a68636f8f2c18511179c56f15e95080c"
}


conn = mysql.connector.connect(user='root', password='tmzkdnxj1', host='34.64.214.96', database ='scout', port='3306')
cursor = conn.cursor()

resTeam = re.get(url = getTeamUrl, headers = headers)
tmpTeamRaw =resTeam.json()
tmpTeamData = tmpTeamRaw['response']

#print(tmpTeamData)
#print(len(tmpTeamData))


#실제 injection넣을 데이터 
insertTeamInfoList =[]

#json으로 으로 pl 데이터 다 받아와서 indexing 후 적재 list에 이중 리스트 구현
for i in range(len(tmpTeamData)):

    #insert 리스트 내부에 인덱싱될 data rabeling
    tmpList = []
    
    tmpList.append(tmpTeamData[i]['team']['name'])
    tmpList.append(tmpTeamData[i]['team']['id'])
    tmpList.append(tmpTeamData[i]['team']['founded'])
    tmpList.append(tmpTeamData[i]['venue']['name'])
    tmpList.append(tmpTeamData[i]['venue']['address'])
    insertTeamInfoList.append(tmpList)


getSeasonSQL = 'select season_id from seasons where season_year = %d'%tmpSeasonYear

#sql문 문제 디버깅
#print(getSeasonSQL)

cursor.execute(getSeasonSQL)
seasonRawData = cursor.fetchall()

insertSeasonId = seasonRawData[0][0]


getLeagueSQL = 'select league_id from league_info where league_name = "%s"' %tmpLeagueName

#sql문 문제 디버깅
#print(getLeagueSQL)

cursor.execute(getLeagueSQL)
leagueRawData = cursor.fetchall()

insertLeagueId = leagueRawData[0][0]

for i in range(len(insertTeamInfoList)):

    getFormationUrl = "https://v3.football.api-sports.io/teams/statistics?season=%d&league=%d&team=%d"%(tmpSeasonYear, tmpLeagueID,insertTeamInfoList[i][1])
    
    #uri 확인
    #print(getFormationUrl)

    tmpFormationRaw = re.get(url = getFormationUrl, headers=headers).json()

    tmpFormationData = tmpFormationRaw['response']['lineups'][0]['formation']
    
    #rawdata확인
    #print(tmpFormationData)
    
    convertFormation = tmpFormationData.replace('-','')

    #print(insertTeamInfoList[i])

    #injection data에 season_id record load
    insertTeamInfoList[i].append(insertSeasonId)

    #injection data에 league_id record load
    insertTeamInfoList[i].append(insertLeagueId)

    insertTeamInfoList[i].append("")
    insertTeamInfoList[i].append("")
    print(insertTeamInfoList[i])

    getFormationSQL = 'select formation_id from formation_info where formation_name = "%s"' %convertFormation
    cursor.execute(getFormationSQL)
    formationRawData = cursor.fetchall()
    insertFormationId = formationRawData[0][0]

    #formation 데이터 확인
    #print("%d : %d"%(i, insertFormationId))

    #injection data에 formation record도 load 
    insertTeamInfoList[i].append(insertFormationId)



















