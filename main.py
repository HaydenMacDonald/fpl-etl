import asyncio
import configparser
import MySQLdb
from mysql.connector import errorcode
from helpers.get_spi_data import get_spi_data
from helpers.get_player_data import get_player_data
from helpers.clean_player_data import clean_player_data
from helpers.prepare_weekly_player_data import prepare_weekly_data
from helpers.delete_data import delete_data
from sql.sql_queries import create_table_queries, drop_table_queries

def process_weekly_data():

    ## Get SPI Match data (local or remote)
    spi_data = get_spi_data()

    ## Get player data (local or remote)
    players = asyncio.get_event_loop().run_until_complete(get_player_data())

    ## Clean player data
    players = clean_player_data(players)

    ## Prepare weekly data
    prepare_weekly_data()


def write_to_db():
    
    ## Write data to db
    write_weekly_data_to_db()

    ## Clear weekly data from local
    # delete_data()

def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Main ETL function
    '''
    ## Parse config file for AWS details
    config = configparser.ConfigParser()
    config.read("db.cfg")

    # Connect to planetscale db
    conn = MySQLdb.connect(
        host     = f"{config['DB']['HOST']}",
        user     = f"{config['DB']['DB_USER']}",
        password = f"{config['DB']['DB_PASSWORD']}",
        db       = f"{config['DB']['DB_NAME']}",
        port     = int(f"{config['DB']['DB_PORT']}"),
        ssl_mode = f"{config['DB']['SSL_MODE']}",
        ssl      = {
            "ca": f"{config['DB']['SSL_CA']}"
        }
    )
    
    # Create cursor
    cur = conn.cursor()

    # Collect and process data
    process_weekly_data()

    # Test
    cur.execute("SELECT CURDATE();")

    # Fetch one result
    row = cur.fetchone()
    print("Current date is: {0}".format(row[0]))
    
    # Process and insert song and artist data
    #write_to_db(cur, conn, filepath='data/song_data', func=process_song_file)
    
    # Close connection to sparkifydb
    conn.close()


if __name__ == "__main__":
    main()