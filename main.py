import asyncio
from helpers.get_spi_data import get_spi_data
from helpers.get_player_data import get_player_data
from helpers.clean_player_data import clean_player_data
from helpers.prepare_weekly_player_data import prepare_weekly_data
from helpers.delete_data import delete_data

def main():

    ## Get SPI Match data (local or remote)
    spi_data = get_spi_data()

    ## Get player data (local or remote)
    players = asyncio.get_event_loop().run_until_complete(get_player_data())

    ## Clean player data
    players = clean_player_data(players)

    ## Prepare weekly data
    prepare_weekly_data()

    ## Write data to db
    

    delete_data()


if __name__ == "__main__":
    main()