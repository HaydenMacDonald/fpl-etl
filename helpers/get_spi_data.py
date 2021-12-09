import pandas as pd
import numpy as np
from datetime import date, datetime
import os 
from pathlib import Path

def get_spi_data():

    directory = "./data/cleaned/spi-matches/"

    ## Target data file
    data_file = f"{directory}spi-matches-{date.today()}.csv"

    if date.weekday(date.today()) == 3:
        
        ## If data doesn't exist, get it
        if not os.path.isfile(data_file): 
            
            ## Read csv from url
            spi_data = pd.read_csv("https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv")

        ## Otherwise, open local copy
        else:
            spi_data = pd.read_csv(data_file, index_col=False)

        ## Filter for Premier League matches
        spi_data = spi_data.loc[(spi_data["season"] == date.today().year) & (spi_data["league"] == "Barclays Premier League")]

        spi_data["team1_code"] = np.select(
            [
                spi_data["team1"]=="Manchester United",
                spi_data["team1"]=="Leeds United",
                spi_data["team1"]=="Arsenal",
                spi_data["team1"]=="Newcastle",
                spi_data["team1"]=="Tottenham Hotspur",
                spi_data["team1"]=="Aston Villa",
                spi_data["team1"]=="Chelsea",
                spi_data["team1"]=="Everton",
                spi_data["team1"]=="Leicester City",
                spi_data["team1"]=="Liverpool",
                spi_data["team1"]=="Southampton",
                spi_data["team1"]=="West Ham United",
                spi_data["team1"]=="Crystal Palace",
                spi_data["team1"]=="Brighton and Hove Albion",
                spi_data["team1"]=="Wolverhampton",
                spi_data["team1"]=="Manchester City",
                spi_data["team1"]=="Norwich City",
                spi_data["team1"]=="Watford",
                spi_data["team1"]=="Burnley",
                spi_data["team1"]=="Brentford"
            ],
            [
                1,
                2,
                3,
                4,
                6,
                7,
                8,
                11,
                13,
                14,
                20,
                21,
                31,
                36,
                39,
                43,
                45,
                57,
                90,
                94
            ],
            default=None
        )

        spi_data["team2_code"] = np.select(
            [
                spi_data["team2"]=="Manchester United",
                spi_data["team2"]=="Leeds United",
                spi_data["team2"]=="Arsenal",
                spi_data["team2"]=="Newcastle",
                spi_data["team2"]=="Tottenham Hotspur",
                spi_data["team2"]=="Aston Villa",
                spi_data["team2"]=="Chelsea",
                spi_data["team2"]=="Everton",
                spi_data["team2"]=="Leicester City",
                spi_data["team2"]=="Liverpool",
                spi_data["team2"]=="Southampton",
                spi_data["team2"]=="West Ham United",
                spi_data["team2"]=="Crystal Palace",
                spi_data["team2"]=="Brighton and Hove Albion",
                spi_data["team2"]=="Wolverhampton",
                spi_data["team2"]=="Manchester City",
                spi_data["team2"]=="Norwich City",
                spi_data["team2"]=="Watford",
                spi_data["team2"]=="Burnley",
                spi_data["team2"]=="Brentford"
            ],
            [
                1,
                2,
                3,
                4,
                6,
                7,
                8,
                11,
                13,
                14,
                20,
                21,
                31,
                36,
                39,
                43,
                45,
                57,
                90,
                94
            ],
            default=None
        )

        spi_data = spi_data[["season", "date", "league_id", "league", "team1", "team2", "spi1", "spi2", "prob1", "prob2", "probtie", "proj_score1", "proj_score2", "importance1", "importance2", "score1", "score2", "xg1", "xg2", "nsxg1", "nsxg2", "adj_score1", "adj_score2", "team1_code", "team2_code"]]

        ## Check if directory exists, if not create directory
        Path(f"{directory}").mkdir(parents=True, exist_ok=True)

        ## Write data to csv
        spi_data.to_csv(data_file, index=False)

        return spi_data