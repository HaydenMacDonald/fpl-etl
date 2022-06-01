# DROP TABLES

player_fixtures_table_drop = "DROP TABLE IF EXISTS player_fixtures;"
players_table_drop = "DROP TABLE IF EXISTS players;"
positions_table_drop = "DROP TABLE IF EXISTS positions;"
teams_table_drop = "DROP TABLE IF EXISTS teams;"
gameweeks_table_drop = "DROP TABLE IF EXISTS gameweeks;"

# CREATE TABLES

player_fixtures_table_create = ("""
CREATE TABLE IF NOT EXISTS player_fixtures (
    ref PRIMARY KEY NOT NULL AUTO_INCREMENT,
    player_id VARCHAR(100),
    fixture_id VARCHAR(100),
    gameweek_id VARCHAR(100),
    season INT,
    team_id INT,
    opponent_team_id INT,
    is_home boolean,
    kickoff_time datetime,
    position_id INT,
    price DOUBLE(4,2),
    last_three_form DOUBLE(4,2),
    minutes INT,
    nineties DOUBLE(4,2)
    goals INT,
    goals_per_90 DOUBLE(4,2),
    xG_per_90 DOUBLE(4,2),
    assists INT,
    assists_per_90 DOUBLE(4,2),
    xA_per_90 DOUBLE(4,2),
    clean_sheets INT,
    clean_sheets_per_90 DOUBLE(4,2),
    goals_conceded INT,
    goals_conceded_per_90 DOUBLE(4,2),
    yellow_cards INT,
    yellow_cards_p90 DOUBLE(4,2),
    red_cards INT,
    red_cards_p90 DOUBLE(4,2),
    play_probability_next_game DOUBLE(4,2),
    play_probability_this_game DOUBLE(4,2),
    bonus_points INT,
    points_per_game DOUBLE(4,2),
    total_points BIGINT,
    team_spi DOUBLE(4,2),
    opponent_spi DOUBLE(4,2),
    win_prob DOUBLE(4,4),
    loss_prob DOUBLE(4,4),
    draw_prob DOUBLE(4,4),
    team_projected_score DOUBLE(4,2),
    opponent_projected_score DOUBLE(4,2),
    fbref JSON,
    actual_points_earned INT
);
""")

players_table_create = ("""
CREATE TABLE IF NOT EXISTS players (
    player_id VARCHAR(100) PRIMARY KEY NOT NULL,
    first_name VARCHAR(150), 
    last_name VARCHAR(150)
);
""")

positions_table_create = ("""
CREATE TABLE IF NOT EXISTS positions (
    position_code INT PRIMARY KEY NOT NULL, 
    position_name VARCHAR(100) NOT NULL,
    position_type VARCHAR(100) NOT NULL
);
""")

teams_table_create = ("""
CREATE TABLE IF NOT EXISTS teams (
    team_id INT PRIMARY KEY NOT NULL, 
    team_name VARCHAR(150) NOT NULL,
    short_name VARCHAR(100) NOT NULL
);
""")

gameweeks_table_create = ("""
CREATE TABLE IF NOT EXISTS gameweeks (
    gameweek_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
    season INT, 
    gameweek_no INT, 
    start_date datetime, 
    end_date datetime,
);
""")

# INSERT RECORDS
player_fixtures_table_insert = ("""
INSERT INTO player_fixtures (
)
VALUES ()
ON CONFLICT (ref) 
DO NOTHING;
""")

players_table_insert = ("""
INSERT INTO players VALUES (%s, %s, %s) 
ON CONFLICT (player_id) 
DO UPDATE SET level=EXCLUDED.level;
""")

positions_table_insert = ("""
INSERT INTO positions VALUES (%s, %s, %s)
ON CONFLICT (position_code) 
DO NOTHING;
""")

teams_table_insert = ("""
INSERT INTO teams VALUES (%s, %s, %s)
ON CONFLICT (team_code) 
DO NOTHING;
""")

gameweeks_table_insert = ("""
INSERT INTO gameweeks VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (gameweek_id) 
DO NOTHING;
""")


# QUERY LISTS
create_table_queries = [player_fixtures_table_create, players_table_create, positions_table_create, teams_table_create, gameweeks_table_create]
drop_table_queries = [player_fixtures_table_drop, players_table_drop, positions_table_drop, teams_table_drop, gameweeks_table_drop]