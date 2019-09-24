from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
from contextlib import closing

class SqlQuery:
    
    def sql_query(self,sql):
        rows = []
        with connect(dbname='sport_user', user='sport_user', password='passw0rd', host='localhost') as conn:
            with conn.cursor(cursor_factory = NamedTupleCursor) as cursor:
                cursor.execute(sql)                
                for row in cursor:
                    rows.append(row)
        return rows

class listLiga(SqlQuery):
    rows = []
    def __init__(self):
        self.rows = self.sql_query_list()  
    
    def sql_query_list(self):
        return self.sql_query('SELECT * FROM liga_hock ORDER BY liga_country, liga_name DESC') 

class teamsName(SqlQuery):
    teams_name = {}
    def __init__(self,teams):
        self.teams_name = self.sql_query_list(teams) 
        # print(teams_name) 
    
    def sql_query_list(self,teams):
        team = "','".join(teams)
        sql = f"SELECT team_cod, team_href, team_image, team_name FROM team_hock WHERE team_cod IN ('{team}')"
        return self.sql_query(sql)

class matchesScore(SqlQuery):
    score = { 'home':{},'away':{} }
    def __init__(self,matches):
        for value in ['home','away']:
            temp_score = self.sql_query_list(matches[value])
            for row in temp_score:
                array = []
                tarr = { 'match': row.score_match }
                array.append(tarr)
                for key in row.score_period.keys():
                    array.append({ key : row.score_period[key] })
                self.score[value][row.score_match_cod] = array

    def sql_query_list(self,cod):
        matches_cod = "','".join(cod)
        sql = f"SELECT score_match_cod, score_match, score_period FROM score_hock WHERE score_match_cod IN ('{ matches_cod }')"
        return self.sql_query(sql)

class matchesList(SqlQuery):
    matches = { 'home':[], 'away':[] }
    teams_name = {}
    matches_cod = { 'home':[],'away':[] }    
    def __init__(self,home,away):
        tteams  = []
        self.matches = self.sql_query_list(home,away)
        for value in ['home','away']:
            for val in self.matches[value]:
                try:
                    self.matches_cod[value].append(val.match_id)
                except:
                    pass
                try:
                    if val.team_left not in tteams:
                        tteams.append(val.team_left)
                except:
                    pass
                try:
                    if val.team_right not in tteams:
                        tteams.append(val.team_right) 
                except:
                    pass 
        if len(tteams) > 0:
            for ttn in teamsName(tteams).teams_name:   
                self.teams_name[ttn.team_cod] = ttn.team_name

        # print(teams_name) 
    
    def sql_query_list(self,home,away):
        sqls = {
            'home' : f"SELECT match_id, date, stage, tournament, status, secondary, team_left, team_right FROM match_hock WHERE team_left = '{home}' ORDER BY date DESC",
            'away' : f"SELECT match_id, date, stage, tournament, status, secondary, team_left, team_right FROM match_hock WHERE team_right = '{away}' ORDER BY date DESC"
        }
        for side in ['home','away']:
            sql = sqls[side]
            self.matches[side] = self.sql_query(sql)
        return self.matches
        
class teamsInLiga(SqlQuery):
    teams = []
    def __init__(self,ligas):
        for val in self.sql_query_list(ligas):
            try:
                if val.team_left not in self.teams:
                    self.teams.append(val.team_left)
            except:
                pass
            try:
                if val.team_right not in self.teams:
                    self.teams.append(val.team_right) 
            except:
                pass            
    
    def sql_query_list(self,ligas):
        liga = "','".join(ligas)
        return self.sql_query(f"SELECT * FROM match_hock WHERE tournament IN ('{liga}')") 