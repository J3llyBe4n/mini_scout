import requests as re
import mysql.connector


tmpTeamId = 42
tmpLeagueId = 39
tmpSeasonYear = 2022


getBaseInfoUri = "https://v3.football.api-sports.io/players/squads?team=%d" %tmpTeamId

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a68636f8f2c18511179c56f15e95080c"
    }

conn = mysql.connector.connect(user ='root', password='tmzkdnxj1', host='34.64.214.96', database ='scout', port = '3306')
cursor = conn.cursor()

resBase = re.get(url = getBaseInfoUri, headers = headers)
tmpBaseRaw = resBase.json()
tmpBaseData = tmpBaseRaw['response'][0]['players']

insertPlayerInfoList =[]

for i in range(len(tmpBaseData)):
    tmpList = []

    tmpList.append(tmpBaseData[i]['name'])
    tmpList.append(tmpBaseData[i]['number'])
    tmpList.append(tmpBaseData[i]['position'])
    tmpList.append(tmpBaseData[i]['photo'])
    insertPlayerInfoList.append(tmpList)

getDetailInfoUri = "https://v3.football.api-sports.io/players?team=%d&season=%d&league=%d" %(tmpTeamId, tmpSeasonYear, tmpLeagueId)

resDetail = re.get(url = getDetailInfoUri, headers = headers)
tmpDetailRaw = resDetail.json()
pageCount = tmpDetailRaw['paging']['total']

mergeRaw = []

for i in range(1, pageCount + 1):

    tmpUri = getDetailInfoUri + '&page=%d' %i
    resTmp = re.get(url = tmpUri, headers = headers)
    tmpRaw = resTmp.json()['response']
    
    for j in range(len(tmpRaw)):
        mergeRaw.append(tmpRaw[j])


for length in range(len(insertPlayerInfoList)):
    for k in range(len(mergeRaw)):
        if mergeRaw[k]['player']['name'] == insertPlayerInfoList[length][0]:
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['firstname'])
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['lastname'])
            #print(mergeRaw[k]['player']['birth']['date'])
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['birth']['date'])
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['height'])
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['weight'])
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['nationality'])

sql1 = 'select team_id from team_info where team_name = "Arsenal";'
cursor.execute(sql1)
result1 = cursor.fetchall()
result2 = result1[0][0]

sql2 = 'insert into player_info (season_id,team_id,first_name,last_name,uniform_number,date_of_birth,main_feet,height,weight,position,player_picture,player_nation) values (%d,%d,"%s","%s",%d,"%s","%s",%d,%d,"%s","%s","%s")' %(tmpSeasonYear,result2,insertPlayerInfoList[5],insertPlayerInfoList[4],insertPlayerInfoList[1],insertPlayerInfoList[6],'',insertPlayerInfoList[7],insertPlayerInfoList[8],insertPlayerInfoList[2],insertPlayerInfoList[3],'')
cursor.execute(sql2)
cursor.commit()

conn.close()


            



    




