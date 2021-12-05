import os
import json
from pathlib import Path

def delete_data(data, directory, filename):

    ## Check if directory exists, if not create directory
    Path(f"{directory}").mkdir(parents=True, exist_ok=True)
    
    ## Then save data
    os.remove(f"{directory}{filename}")