import requests as re
import mysql.connector


tmpTeamId = 42
tmpLeagueId = 39
tmpSeasonYear = 2022


getBaseInfoUri = "https://v3.football.api-sports.io/players/squads?team=%d" %tmpTeamId

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a86d420d0d8840c8e722e16cf9742f7b"
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
    # tmpList.append(tmpBaseData[i]['number'])
    # 등번호에 None 값이 있음
    tmpNumber = tmpBaseData[i]['number']
    if tmpNumber is not None:
        tmpNumber = tmpNumber
    else :
        tmpNumber = 0
    tmpList.append(tmpNumber)
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
            insertPlayerInfoList[length]
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['firstname'])
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['lastname'])
            #print(mergeRaw[k]['player']['birth']['date'])
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['birth']['date'])            
            # Height 값에 None 값이 존재해서 조건문 사용
            tmpHeight = mergeRaw[k]['player']['height']
            if tmpHeight is not None:
                tmpHeight = tmpHeight.replace(' cm', '')
            else :
                tmpHeight = 0
            insertPlayerInfoList[length].append(int(tmpHeight))
            # Weight 값에 None 값이 존재해서 조건문 사용
            tmpWeight = mergeRaw[k]['player']['weight']
            if tmpWeight is not None:
                tmpWeight = tmpWeight.replace(' kg','')
            else :                
                tmpWeight = 0
            insertPlayerInfoList[length].append(int(tmpWeight))
            insertPlayerInfoList[length].append(mergeRaw[k]['player']['nationality'])

# team_id 받아오기
sql1 = 'select team_id from team_info where team_name = "Arsenal";'
cursor.execute(sql1)
result1 = cursor.fetchall()
insertTeamId = result1[0][0]

<<<<<<< HEAD
sql2 = 'insert into player_info (season_id,team_id,first_name,last_name,uniform_number,date_of_birth,main_feet,height,weight,position,player_picture,player_nation) values (%d,%d,"%s","%s",%d,"%s","%s",%d,%d,"%s","%s","%s")' %(tmpSeasonYear,result2,insertPlayerInfoList[5],insertPlayerInfoList[4],insertPlayerInfoList[1],insertPlayerInfoList[6],'',insertPlayerInfoList[7],insertPlayerInfoList[8],insertPlayerInfoList[2],insertPlayerInfoList[3],insertPlayerInfoList[9])
=======
# season_id 받아오기
sql2 = 'select season_id from seasons where season_year = %d' %tmpSeasonYear
>>>>>>> f4cb748c6e90c6a3b90510234ff5cfecc7e31bff
cursor.execute(sql2)
result2 = cursor.fetchall()
insertSeasonId = result2[0][0]

# 실제 모든레코드 insert 구문
for n in range(len(insertPlayerInfoList)):
    sql3 = 'insert into player_info (season_id,team_id,first_name,last_name,uniform_number,date_of_birth,main_feet,height,weight,position,player_picture,player_nation) values (%d,%d,"%s","%s",%d,"%s","%s",%d,%d,"%s","%s","%s")' %(insertSeasonId,insertTeamId,insertPlayerInfoList[n][5],insertPlayerInfoList[n][4],insertPlayerInfoList[n][1],insertPlayerInfoList[n][6],'',insertPlayerInfoList[n][7],insertPlayerInfoList[n][8],insertPlayerInfoList[n][2],insertPlayerInfoList[n][3],insertPlayerInfoList[n][9])
    cursor.execute(sql3)

conn.commit()

conn.close()
