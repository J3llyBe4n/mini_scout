import requests
import mysql.connector

leagueCountry = "Italy"
leagueSeason = 2022
leagueName = "Serie A"


conn = mysql.connector.connect(user='root', password='tmzkdnxj1', host='34.64.214.96', database ='scout', port='3306')
cursor = conn.cursor()

url = "https://v3.football.api-sports.io/leagues?name=%s&country=%s&season=%d" %(leagueName, leagueCountry, leagueSeason)
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "a68636f8f2c18511179c56f15e95080c"
    }

data = requests.request("GET", url, headers=headers).json()

# response 안에 실제 데이터가 있어서 그거만 빼오기
reveil = data['response']

# reveil의 0번째 index의 적재되어있는 자료형은 dict
# 해당 dict 내부에 key값이 league dict를 dict 로 적재
# dict는 dictionary 형태의 key값이 name인 값을 최종 변수에 넣음

tmpSeason = reveil[0]['seasons'][-1]['year']
tmpCountry = reveil[0]['country']['name']

#season_year record를 통해서 db 내 id 값 찾기
getYearIdSQL = 'select season_id from seasons where season_year = %d' %tmpSeason
cursor.execute(getYearIdSQL)
tmpyear_id = cursor.fetchall()
insertSeasonId = tmpyear_id[0][0]

# country_name record를 통해 db내 id값 찾기
getCountryIDSQL = 'select distinct country_id from country_info where country_name = "%s"' %tmpCountry
cursor.execute(getCountryIDSQL)
tmpcountry_id = cursor.fetchall()
insertCountryId = tmpcountry_id[0][0]

# api 내에서 league_name 을 찾기
insertName = reveil[0]['league']['name']

finalList =[]

finalList.append(insertName)
finalList.append(insertCountryId)
finalList.append(insertSeasonId)

injectDataSQL = 'insert into league_info (season_id, nation_id, league_name, league_created, league_team_count, league_round_count, api_league_id) values (%d, %d, "%s", %d, %d, %d, %d)' %(insertSeasonId,insertCountryId,insertName,0,0,0,0)


cursor.execute(injectDataSQL)
cursor.fetchall()
conn.commit()

conn.close()



