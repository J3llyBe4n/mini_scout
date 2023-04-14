import requests as re
import mysql.connector
import time
headers={
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "a68636f8f2c18511179c56f15e95080c"
    }

conn = mysql.connector.connect(user='root', password='tmzkdnxj1', host='34.64.214.96', database ='scout', port='3306')
cursor = conn.cursor()
# season_year 담아둘 빈 리스트 생성
SeasonYearList = []
# db에서 시즌년도 값 쭉 받아오기
getSeasonYearSql = 'select season_year from seasons'
cursor.execute(getSeasonYearSql)
tmpSeasonYear = cursor.fetchall()
# getSeasonYear 쿼리문으로 받아온 값 인덱싱해서 SeasonYearList에 append
for i in range(len(tmpSeasonYear)-1):
    SeasonYearList.append(tmpSeasonYear[i][0])
print(SeasonYearList)

# 각 리그 api_league_id를 받을 빈 리스트 생성
ApiLeagueIdList = []
# db에서 api_league_id 값 받아오기
getApiLeagueId = 'select api_league_id from hidden_league_id'
cursor.execute(getApiLeagueId)
tmpApiLeagueId = cursor.fetchall()
# getApiLeagueId 쿼리문으로 받아온 값 인덱싱해서 ApiLeagueIdList에 append
for j in range(len(tmpApiLeagueId)):
    ApiLeagueIdList.append(tmpApiLeagueId[i][0])
print(ApiLeagueIdList)

for k in range(len(ApiLeagueIdList)):
    
    for l in range(len(SeasonYearList)):
        if k % 2 == 1:
            print('wait for 120s')
            time.sleep(120)
            print('have waited 120s. 다시 일해라!')
        else :
            pass
        url = "https://v3.football.api-sports.io/standings?season=%d&league=%d" %(SeasonYearList[l], ApiLeagueIdList[k])
        resp = re.get(url=url, headers=headers).json()
        tmpData = resp['response'][0]['league']['standings'][0]
        # api에서 받은 값을 담을 빈 리스트 생성 -> 이중 리스트가 될 것임 -> ex) [['Manchester United', 1],['Arsenal',2],,,,]
        tmpRankData = []
        # 최종 insert할 데이터를 담는 빈 리스트 생성 -> 이중 리스트가 될 것임 -> ex) [[1,1],[2,2],,,,] <- [[팀ID,순위],[팀ID,순위],,,,]
        insertRankData = []
        
        # api에서 필요한 값 tmpRankData에 넣기
        for m in range(len(tmpData)):
            # tmpRankData가 이중리스트가 되어야 하기 때문에 한 사이클 마다 tmpRankData에 append할 빈 리스트 생성
            tmptmpRankData = []
            
            tmptmpRankData.append(tmpData[m]['team']['name'])
            tmptmpRankData.append(tmpData[m]['rank'])
            
            # tmpRankData에 append
            tmpRankData.append(tmptmpRankData)
        # season_id 가져오기 -> season_year 값 season_id로 convert해줘야됨
        getSeasonIdSql = 'select season_id from seasons where season_year=%d' %SeasonYearList[l]
        cursor.execute(getSeasonIdSql)
        tmpSeasonId = cursor.fetchall()
        season_id = tmpSeasonId[0][0]
        
        # 받아온 season_id와 api를 통해 받아온 team_name으로 team_id 값 받아오기 + 최종 insert할 insertRankData 리스트에 값 넣기
        for n in range(len(tmpRankData)):
            # insertRankData가 이중리스트가 되어야 하기 때문에 한 사이클 마다 insertRankData에 append할 빈 리스트 생성
            tmpinsertRankData = []
            # season_id와 team_name으로 team_id값 받아오기
            getTeamIdSql = 'select team_id from team_info where season_id=%d and team_name="%s"' %(season_id,tmpRankData[n][0])
            cursor.execute(getTeamIdSql)
            tmpTeamId = cursor.fetchall()
            team_id = tmpTeamId[0][0]
            
            # tmpinsertRankData에 team_id,rank 값 append)
            tmpinsertRankData.append(team_id)
            tmpinsertRankData.append(tmpRankData[n][1])
            # insertRankData에 tmpinsertRankData값 append)
            insertRankData.append(tmpinsertRankData)
