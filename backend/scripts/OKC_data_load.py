import psycopg2
import json
import datetime

try:
    conn = psycopg2.connect( #Connects to PostgreSQL database
        dbname="okc",
        user="okcapplicant",
        password="thunder",
        host="localhost",
        port="5432"
    )

except Exception as e:
    print("Error:", e)

#Opens json files
with open("../raw_data/players.json") as f:  # Accesses player data from json file
    playerData = json.load(f)
with open("../raw_data/games.json") as f:  # Accesses game data from json file
    gameData = json.load(f)
with open("../raw_data/teams.json") as f:  # Accesses team data from json file
    teamData = json.load(f)

cursor = conn.cursor()

#inserts team data into database
for team in teamData: 
    cursor.execute("""
        INSERT INTO teams (team_id, name)
        VALUES (%s, %s)
        ON CONFLICT (team_id) DO NOTHING
    """, (team["team_id"], team["name"]))

#inserts game data into database
for game in gameData:
    game_date = datetime.datetime.strptime(game["date"], "%Y-%m-%d").date()
    cursor.execute("""
        INSERT INTO games (game_id, date)
        VALUES (%s, %s)
        ON CONFLICT (game_id) DO NOTHING
   """, (game["id"], game_date))

#inserts player data into database
for player in playerData:
    player_id = player["player_id"]
    cursor.execute("""
        INSERT INTO players (name, team_id, player_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (player_id) DO NOTHING
    """, (player["name"], player["team_id"], player_id))
    #inserts nested shot list within player
    for shot in player["shots"]:
        cursor.execute("""
            INSERT INTO shots (shot_id, points, shooting_foul_drawn, shot_loc_x, shot_loc_y, game_id, action_type, player_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (shot_id) DO NOTHING
        """, (shot["id"], shot["points"], shot["shooting_foul_drawn"], shot["shot_loc_x"], shot["shot_loc_y"], shot["game_id"], shot["action_type"], player_id))
    #inserts nested pass list
    for _pass in player["passes"]:
        cursor.execute("""
            INSERT INTO passes (pass_id, completed_pass, potential_assist, turnover, ball_start_loc_x, ball_start_loc_y, ball_end_loc_x, ball_end_loc_y, game_id, action_type, player_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (pass_id) DO NOTHING
        """, (_pass["id"], _pass["completed_pass"], _pass["potential_assist"], _pass["turnover"], _pass["ball_start_loc_x"], _pass["ball_start_loc_y"], _pass["ball_end_loc_x"], _pass["ball_end_loc_y"], _pass["game_id"], _pass["action_type"], player_id))
    #inserts nested turnover list
    for turnover in player["turnovers"]:
        cursor.execute("""
            INSERT INTO turnovers (turnover_id, tov_loc_x, tov_loc_y, game_id, action_type, player_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (turnover_id) DO NOTHING
        """, (turnover["id"], turnover["tov_loc_x"], turnover["tov_loc_y"], turnover["game_id"], turnover["action_type"], player_id))

conn.commit()
cursor.close()
conn.close()