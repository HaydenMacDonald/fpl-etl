import datetime
import dateutil.parser as dparser
import os
import json
import pandas as pd
from helpers.write_player_data import write_player_data

def prepare_weekly_data():

    # cleaned directories
    players_path = "./data/cleaned/players/"
    spi_path = "./data/cleaned/spi-matches/"
    fbref_path = "./data/cleaned/fbref/"

    # Scan cleaned/players directory
    player_thursdays = get_thursday_files(players_path)
    spi_thursdays = get_thursday_files(spi_path)
    # fbref_path = get_thursday_files(fbref_path)

    # For each file, transform player data into weekly format
    weekly_data = []
    for file in player_thursdays:
        weekly_format(players_path, spi_path, file, weekly_data)

    # Write data
    write_player_data(weekly_data, "./data/cleaned/weekly-data/", f"{datetime.date.today()}.json")


def weekly_format(players_path, spi_path, this_week_file, result_list):

    ## Create this gameweek's data file paths
    this_week_player_file_path = get_this_gameweek_data_file_path(players_path, "players", this_week_file)
    spi_file_path = get_this_gameweek_data_file_path(spi_path, "spi-matches", this_week_file, file_ext=".csv")

    ## Get next gameweek data file
    next_week_player_file_path = get_next_gameweek_data_file_path(players_path, "players", this_week_file)

    # If exists, open json files
    if this_week_player_file_path is not None and next_week_player_file_path is not None and spi_file_path is not None: 
        if os.path.isfile(this_week_player_file_path) and os.path.isfile(next_week_player_file_path) and os.path.isfile(spi_file_path):
            with open(this_week_player_file_path) as this_week_json, open(next_week_player_file_path) as next_week_json, open(spi_file_path) as spi_csv:
                players = json.load(this_week_json)
                next_week = json.load(next_week_json)
                spi_data = pd.read_csv(spi_csv, index_col=False)

                ## For each player object in players array
                for player in players:
                    
                    ## Set default value to None for following fields
                    player.setdefault("player_code", None)
                    player.setdefault("web_name", None)
                    team_code = player.get("team_code", None)
                    game_date = datetime.datetime.strptime(player.get("fixtures", {})[0].get("kickoff_time"), "%Y-%m-%d %H:%M:%S").date()

                    ## Convert date column to date type
                    spi_data["date"] = pd.to_datetime(spi_data["date"], format="%Y-%m-%d").dt.date

                    # Get spi data
                    spi_week = spi_data[((spi_data["date"] == game_date) & (spi_data["team1_code"] == team_code)) | ((spi_data["date"] == game_date) &  (spi_data["team2_code"] == team_code))]

                    ## Assign resulting data to weekly_data
                    player_dict = dict(
                        player_code = player.get("player_code"), 
                        web_name = player.get("web_name"),
                        season = player.get("season", "2021/22"),
                        next_gameweek = player.get("fixtures", {})[0].get("event_name"),
                        kickoff_time = player.get("fixtures", {})[0].get("kickoff_time"),
                        team_code = team_code,
                        opponent_code = int(spi_week["team2_code"].values[0]) if spi_week["team1_code"].values[0] == team_code else int(spi_week["team1_code"].values[0]),
                        opponent_standing = player.get("fixtures", {})[0].get("team_a") if player.get("fixtures", {})[0].get("is_home") == True else player.get("fixtures", {})[0].get("team_h"),
                        is_home = player.get("fixtures", {})[0].get("is_home"),
                        position = player.get("element_type"), 
                        price = player.get("price"),
                        total_points = player.get("total_points"),
                        form = float(player.get("form")), 
                        points_per_game = float(player.get("points_per_game")),
                        minutes = player.get("minutes"),
                        nineties = player.get("minutes", 0) / 90,
                        yellow_cards_p90 = player.get("yellow_cards", 0) / (player.get("minutes", 0) / 90) if player.get("minutes", 0) > 0 else 0,
                        red_cards_p90 = player.get("red_cards", 0) / (player.get("minutes", 0) / 90) if player.get("minutes", 0) > 0 else 0,
                        chance_of_playing_next_round = player.get("chance_of_playing_next_round"), 
                        chance_of_playing_this_round = player.get("chance_of_playing_this_round"),
                        next_week_fixture_id = player.get("fixtures", {})[0].get("id"),
                        next_week_fixture_history = [next_week_players.get("history", {}) for next_week_players in next_week if next_week_players.get("player_code") == player.get("player_code")][0],
                        team_spi = spi_week["spi1"].values[0] if spi_week["team1_code"].values[0] == team_code else spi_week["spi2"].values[0],
                        opponent_spi = spi_week["spi2"].values[0] if spi_week["team1_code"].values[0] == team_code else spi_week["spi1"].values[0],
                        win_prob = spi_week["prob1"].values[0] if spi_week["team1_code"].values[0] == team_code else spi_week["prob2"].values[0],
                        loss_prob = spi_week["prob2"].values[0] if spi_week["team1_code"].values[0] == team_code else spi_week["prob1"].values[0],
                        draw_prob = spi_week["probtie"].values[0],
                        team_projected_score = spi_week["proj_score1"].values[0] if spi_week["team1_code"].values[0] == team_code else spi_week["proj_score2"].values[0],
                        opponent_projected_score = spi_week["proj_score2"].values[0] if spi_week["team1_code"].values[0] == team_code else spi_week["proj_score1"].values[0],
                        #spi = spi_week.to_dict(),
                        fbref = {}
                    )

                    ## Retrieve the actual points earned from next week's data
                    player_dict.setdefault("actual_points_earned", [fixture.get("total_points") for fixture in player_dict.get("next_week_fixture_history") if fixture.get("fixture") == player_dict.get("next_week_fixture_id")][0])

                    ## Remove unecessary data
                    player_dict = remove_key(player_dict, "next_week_fixture_history")
                    player_dict = remove_key(player_dict, "next_week_fixture_id")

                    ## Append player
                    result_list.append(player_dict)

                return result_list

        ## If file does not exist, pass
        else:
            pass

    ## If any file path is None, pass
    else:
        pass


def get_thursday_files(path):

    # Scan directory
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # Extract files extracted on a thursday
    thursdays = [file for file in files if thursday_date_check(file)]

    return thursdays

def thursday_date_check(str_val):

    try:
        result = dparser.parse(str_val, fuzzy=True) # Parse string for ISO date
        if result is not None:
            if result.date().weekday() == 3:  # if date is Thursday, return True
                return True
    except:
        pass
    return False


def get_next_gameweek_data_file_path(path, prefix, file_name):

    try:
        result = dparser.parse(file_name, fuzzy=True) # Parse string for ISO date
        if result is not None:
            delta = datetime.timedelta(days=7)
            next_week = result.date() + delta
            if os.path.isfile(f"{path}{prefix}-{next_week}.json"):  # If next week's data file exists return file name
                return f"{path}{prefix}-{next_week}.json"
            elif os.path.isfile(f"{path}{prefix}-{next_week+delta}.json"):
                return f"{path}{prefix}-{next_week+delta}.json"
    except:
        pass
    return None


def get_this_gameweek_data_file_path(path, prefix, file_name, file_ext=".json"):

    try:
        result = dparser.parse(file_name, fuzzy=True) # Parse string for ISO date
        if result is not None:
            this_gameweek = result.date()
            if os.path.isfile(f"{path}{prefix}-{this_gameweek}{file_ext}"):  # If data file exists, return file name
                return f"{path}{prefix}-{this_gameweek}{file_ext}"
    except:
        pass
    return None


def remove_key(d, key):
    r = d.copy()
    del r[key]
    return r