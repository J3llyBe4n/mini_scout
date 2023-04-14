import mysql.connector

tmpTeamId = []
tmpLeagueId = 39
tmpSeasonYear = 2022

conn = mysql.connector.connect(user ='root', password='tmzkdnxj1', host='34.64.214.96', database ='scout', port = '3306')
cursor = conn.cursor()

getTeamApiIdSql = 'SELECT DISTINCT hidden_team_id.api_team_id FROM team_info  JOIN hidden_team_id ON team_info.team_name = hidden_team_id.team_name  WHERE team_info.league_id = 1 AND team_info.season_id = 8;'
cursor.execute(getTeamApiIdSql)
tmpTeamRaw = cursor.fetchall()

for i in range(len(tmpTeamRaw)):
    tmpTeamId.append(tmpTeamRaw[i][0])

print(tmpTeamId)


