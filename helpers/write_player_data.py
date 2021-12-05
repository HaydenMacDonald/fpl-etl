import json
from pathlib import Path

def write_player_data(data, directory, filename):

    ## Check if directory exists, if not create directory
    Path(f"{directory}").mkdir(parents=True, exist_ok=True)
    
    ## Then save data
    with open(f"{directory}{filename}", "w") as outfile:
        json.dump(data, outfile, ensure_ascii = True, indent = 4, separators=(",", ":"))