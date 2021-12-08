# DROP TABLES

player_gameweeks_table_drop = "DROP TABLE IF EXISTS player_gameweeks;"
players_table_drop = "DROP TABLE IF EXISTS players;"
positions_table_drop = "DROP TABLE IF EXISTS positions;"
teams_table_drop = "DROP TABLE IF EXISTS teams;"
gameweeks_table_drop = "DROP TABLE IF EXISTS gameweeks;"

# CREATE TABLES

player_gameweek_table_create = ("""
CREATE TABLE IF NOT EXISTS player_gameweeks (
    ref PRIMARY KEY NOT NULL AUTO_INCREMENT,
    season int,
    next_gameweek int, 
    kickoff_time datetime,
    team_code int,
    opponent_code int,
    opponent_standing int,
    is_home boolean,
    position int,
    price DOUBLE PRECISION(4,2),
    total_points int,
    form DOUBLE PRECISION(4,2),
    points_per_game DOUBLE PRECISION(4,2),
    minutes int,
    nineties DOUBLE PRECISION(4,2),
    yellow_cards_p90 DOUBLE PRECISION(4,2),
    red_cards_p90 DOUBLE PRECISION(4,2),
    chance_of_playing_next_round DOUBLE PRECISION(4,2),
    chance_of_playing_this_round DOUBLE PRECISION(4,2),
    team_spi DOUBLE PRECISION(4,2),
    opponent_spi DOUBLE PRECISION(4,2),
    win_prob DOUBLE PRECISION(4,4),
    loss_prob DOUBLE PRECISION(4,4),
    draw_prob DOUBLE PRECISION(4,4),
    team_projected_score DOUBLE PRECISION(4,2),
    opponent_projected_score DOUBLE PRECISION(4,2),
    fbref JSON,
    actual_points_earned int
);
""")

player_table_create = ("""
CREATE TABLE IF NOT EXISTS players (
    player_code int PRIMARY KEY NOT NULL, 
    first_name varchar(150), 
    last_name varchar(150)
);
""")

position_table_create = ("""
CREATE TABLE IF NOT EXISTS positions (
    position_code int PRIMARY KEY NOT NULL, 
    position_name varchar(100) NOT NULL
);
""")

team_table_create = ("""
CREATE TABLE IF NOT EXISTS teams (
    team_code int PRIMARY KEY NOT NULL, 
    team_name varchar(150) NOT NULL,
);
""")

gameweeks_table_create = ("""
CREATE TABLE IF NOT EXISTS gameweeks (
    ref int PRIMARY KEY NOT NULL AUTO_INCREMENT, 
    season int, 
    gameweek_number int, 
    start_date datetime, 
    end_date datetime,
);
""")

# INSERT RECORDS
player_gameweek_table_insert = ("""
INSERT INTO player_gameweeks (
    season, 
    next_gameweek, 
    kickoff_time,
    team_code,
    opponent_code,
    opponent_standing,
    is_home,
    position,
    price,
    total_points,
    form,
    points_per_game,
    minutes,
    nineties,
    yellow_cards_p90,
    red_cards_p90,
    chance_of_playing_next_round,
    chance_of_playing_this_round,
    team_spi,
    opponent_spi,
    win_prob,
    loss_prob,
    draw_prob,
    team_projected_score,
    opponent_projected_score,
    fbref,
    actual_points_earned
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (ref) 
DO NOTHING;
""")

player_table_insert = ("""
INSERT INTO players VALUES (%s, %s, %s) 
ON CONFLICT (player_code) 
DO UPDATE SET level=EXCLUDED.level;
""")

position_table_insert = ("""
INSERT INTO positions VALUES (%s, %s)
ON CONFLICT (position_code) 
DO NOTHING;
""")

team_table_insert = ("""
INSERT INTO teams VALUES (%s, %s)
ON CONFLICT (team_code) 
DO NOTHING;
""")

gameweeks_table_insert = ("""
INSERT INTO gameweeks VALUES (%s, %s, %s, %s, %s) 
ON CONFLICT (ref) 
DO NOTHING;
""")


# QUERY LISTS
create_table_queries = [player_gameweek_table_create, player_table_create, position_table_create, team_table_create, gameweeks_table_create]
drop_table_queries = [player_gameweeks_table_drop, players_table_drop, positions_table_drop, teams_table_drop, gameweeks_table_drop]