import aiohttp
from fpl import FPL
from datetime import date
import os
import json
from helpers.write_player_data import write_player_data

async def get_player_data():

    ## Target data file
    directory = "./data/raw/players/"
    filename = f"players-{date.today()}.json"

    ## If data doesn"t exist, get it
    if not os.path.isfile(f"{directory}{filename}"):
        
        async with aiohttp.ClientSession() as session:
            ## Instantiate session
            fpl = FPL(session)

            ## Fetch player data with async request
            players = await fpl.get_players(include_summary=True, return_json=True)

            ## Write player data as json file
            write_player_data(players, directory, filename)
    
    ## Otherwise, access local copy
    else:
        with open(f"{directory}{filename}") as json_file:
            players = json.load(json_file)
    
    return players