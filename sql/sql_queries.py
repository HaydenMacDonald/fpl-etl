# DROP TABLES

player_fixtures_table_drop = "DROP TABLE IF EXISTS player_fixtures;"
players_table_drop = "DROP TABLE IF EXISTS players;"
positions_table_drop = "DROP TABLE IF EXISTS positions;"
player_positions_table_drop = "DROP TABLE IF EXISTS player_positions;"
teams_table_drop = "DROP TABLE IF EXISTS teams;"
player_teams_table_drop = "DROP TABLE IF EXISTS player_teams;"
fixtures_table_drop = "DROP TABLE IF EXISTS fixtures;"
gameweeks_table_drop = "DROP TABLE IF EXISTS gameweeks;"
seasons_table_drop = "DROP TABLE IF EXISTS seasons;"

# CREATE TABLES

player_fixtures_table_create = ("""
CREATE TABLE IF NOT EXISTS player_fixtures (
    player_id VARCHAR(100) NOT NULL,
    fixture_id VARCHAR(100) NOT NULL,
    price DOUBLE(4,2),
    minutes INT,
    nineties DOUBLE(4,2),
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
    play_probability_this_game DOUBLE(4,2),
    play_probability_next_game DOUBLE(4,2),
    team_spi DOUBLE(4,2),
    opponent_spi DOUBLE(4,2),
    win_prob DOUBLE(4,4),
    loss_prob DOUBLE(4,4),
    draw_prob DOUBLE(4,4),
    team_projected_score DOUBLE(4,2),
    opponent_projected_score DOUBLE(4,2),
    fbref JSON,
    bonus_points INT,
    last_three_form DOUBLE(4,2),
    points_per_game DOUBLE(4,2),
    total_points INT,
    actual_points_earned INT,
    PRIMARY KEY (player_id, fixture_id)
)   ENGINE=INNODB;
""")

players_table_create = ("""
CREATE TABLE IF NOT EXISTS players (
    player_id VARCHAR(100) NOT NULL PRIMARY KEY,
    first_name VARCHAR(150), 
    last_name VARCHAR(150)
)   ENGINE=INNODB;
""")

positions_table_create = ("""
CREATE TABLE IF NOT EXISTS positions (
    position_id INT NOT NULL PRIMARY KEY, 
    position_name VARCHAR(100) NOT NULL,
    position_type VARCHAR(100) NOT NULL
)   ENGINE=INNODB;
""")

player_positions_table_create = ("""
CREATE TABLE IF NOT EXISTS player_positions (
    position_id INT,
    player_id VARCHAR(100),
    from DATE,
    to DATE,
    PRIMARY KEY (position_id, player_id)
)   ENGINE=INNODB;
""")

teams_table_create = ("""
CREATE TABLE IF NOT EXISTS teams (
    team_id INT NOT NULL PRIMARY KEY, 
    team_name VARCHAR(150) NOT NULL,
    short_name VARCHAR(100) NOT NULL
)   ENGINE=INNODB;
""")

player_teams_table_create = ("""
CREATE TABLE IF NOT EXISTS player_teams (
    team_id INT,
    player_id VARCHAR(100),
    from DATE,
    to DATE,
    PRIMARY KEY (team_id, player_id)
)   ENGINE=INNODB;
""")

fixtures_table_create = ("""
CREATE TABLE IF NOT EXISTS fixtures (
    fixture_id INT NOT NULL PRIMARY KEY,
    home_team_id INT,
    away_team_id INT,
    kickoff_time DATETIME,
    gameweek_id INT
)   ENGINE=INNODB;
""")

gameweeks_table_create = ("""
CREATE TABLE IF NOT EXISTS gameweeks (
    gameweek_id INT NOT NULL PRIMARY KEY, 
    season INT, 
    gameweek_no INT, 
    start_date DATETIME, 
    end_date DATETIME
)   ENGINE=INNODB;
""")

seasons_table_create = ("""
CREATE TABLE IF NOT EXISTS seasons (
    season INT NOT NULL PRIMARY KEY, 
    start_date DATE, 
    end_date DATE
)   ENGINE=INNODB;
""")


# INSERT RECORDS
player_fixtures_table_insert = ("""
INSERT INTO player_fixtures (
    player_id,
    fixture_id,
    gameweek_id,
    season,
    team_id,
    opponent_team_id,
    is_home,
    kickoff_time,
    position_id,
    price,
    minutes,
    nineties,
    goals,
    goals_per_90,
    xG_per_90,
    assists,
    assists_per_90,
    xA_per_90,
    clean_sheets,
    clean_sheets_per_90,
    goals_conceded,
    goals_conceded_per_90,
    yellow_cards,
    yellow_cards_p90,
    red_cards,
    red_cards_p90,
    play_probability_next_game,
    play_probability_this_game,
    team_spi,
    opponent_spi,
    win_prob,
    loss_prob,
    draw_prob,
    team_projected_score,
    opponent_projected_score,
    fbref,
    bonus_points,
    last_three_form,
    points_per_game,
    total_points,
    actual_points_earned
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (player_id, fixture_id) 
DO NOTHING;
""")

players_table_insert = ("""
INSERT INTO players(
    player_id,
    first_name, 
    last_name
)
VALUES (%s, %s, %s) 
ON CONFLICT (player_id) 
DO NOTHING;
""")

positions_table_insert = ("""
INSERT INTO positions (
    position_id, 
    position_name,
    position_type
)
VALUES (%s, %s, %s)
ON CONFLICT (position_id) 
DO NOTHING;
""")

player_positions_table_insert = ("""
INSERT INTO positions (
    position_id,
    player_id,
    from,
    to
)
VALUES (%s, %s, %s, %s)
ON CONFLICT (position_id, player_id) 
DO NOTHING;
""")

teams_table_insert = ("""
INSERT INTO teams (
    team_id, 
    team_name,
    short_name
)
VALUES (%s, %s, %s)
ON CONFLICT (team_id) 
DO NOTHING;
""")

player_teams_table_insert = ("""
INSERT INTO player_teams (
    team_id,
    player_id,
    from,
    to
)
VALUES (%s, %s, %s, %s)
ON CONFLICT (team_id, player_id) 
DO NOTHING;
""")


fixtures_table_insert = ("""
INSERT INTO fixtures (
    fixture_id,
    home_team_id,
    away_team_id,
    kickoff_time,
    gameweek_id
)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (fixture_id) 
DO NOTHING;
""")

gameweeks_table_insert = ("""
INSERT INTO gameweeks (
    gameweek_id, 
    season, 
    gameweek_no, 
    start_DATE, 
    end_date
)
VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (gameweek_id) 
DO NOTHING;
""")

seasons_table_insert = ("""
INSERT INTO seasons (
    season,
    season_name,
    start_DATE, 
    end_date
)
VALUES (%s, %s, %s, %s) 
ON CONFLICT (season) 
DO NOTHING;
""")


# QUERY LISTS
create_table_queries = [player_fixtures_table_create, players_table_create, positions_table_create, player_positions_table_create, teams_table_create, player_teams_table_create, fixtures_table_create, gameweeks_table_create, seasons_table_create]
drop_table_queries = [player_fixtures_table_drop, players_table_drop, positions_table_drop, player_positions_table_drop, teams_table_drop, player_teams_table_drop, fixtures_table_drop, gameweeks_table_drop, seasons_table_drop]
insert_table_queries = [player_fixtures_table_insert, players_table_insert, positions_table_insert, player_positions_table_insert, teams_table_insert, player_teams_table_insert, fixtures_table_insert, gameweeks_table_insert, seasons_table_insert]
settings_queries = ["set global workload = 'olap';", 'set @@sql_mode = (select replace(@@sql_mode,"ONLY_FULL_GROUP_BY", ""));']