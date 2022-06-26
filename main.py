import asyncio
import configparser
import mysql.connector
from mysql.connector import errorcode
from helpers.get_spi_data import get_spi_data
from helpers.get_player_data import get_player_data
from helpers.clean_player_data import clean_player_data
from helpers.prepare_weekly_player_data import prepare_weekly_data
from helpers.delete_data import delete_data
from sql.sql_queries import *

def process_data(filepath, func):
    '''
    Provided a filepath and a processing function (i.e. process_*_data) to process all files in a given filepath
    '''
    # get all files in path
    data_files = get_files_in_path(filepath, '*.csv')
    print(data_files)

    # iterate over files and process
    for i, datafile in enumerate(data_files, 1):
        func(datafile)
        print('{}/{} files processed.'.format(i, len(data_files)))


def process_weekly_data():

    ## Get SPI Match data (local or remote)
    spi_data = get_spi_data()

    ## Get player data (local or remote)
    players = asyncio.get_event_loop().run_until_complete(get_player_data())

    ## Clean player data
    players = clean_player_data(players)

    ## Prepare weekly data
    prepare_weekly_data()


def process_player_fixture_data(datafile):
    """
    Import, clean, and insert player-fixture data into db 
    """
    # open file
    #df = pd.read_csv(datafile)

    ## Remove NAs
    #df = df[df['player-fixture-id'].notna()]

    i = 1
    for df in rows_generator(df):
        print(f'Player Fixture Split #{i}')
        
        # Parse data from df
        data = df[[
            # "click_date",
            # "masked_id",
            # "apr_clicked",
            # "eligibility_clicked"
        ]].values.tolist()

        print(len(data))

        ## Insert data
        insert_data(player_fixtures_table_insert, data)

        ## Finish by incrementing for next loop
        i += 1


def insert_data(insert_query, data):
    """
    Insert a rows of data using its corresponding insert query
    """
    # Insert credit_reports data
    try:
        cur, conn = make_connection()
        cur.executemany(insert_query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Failed to insert rows: {err}")
        exit(1)
    # Close connection
    conn.close()


def create_tables():
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    try:
        cur, conn = make_connection()
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
    except mysql.connector.Error as err:
        print(f"Failed to create tables: {err}")
        exit(1)

    # Close connection
    conn.close()


def drop_tables():
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    try:
        cur, conn = make_connection()
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
            print(f"Dropped tables.")
    except mysql.connector.Error as err:
        print(f"Failed to drop tables: {err}")
        exit(1)

    # Close connection
    conn.close()


def make_connection():
    """
    Make a connection to the database using db.cfg
    Return the cursor and connection objects required for database operations
    """
    ## Parse config file for database details
    config = configparser.ConfigParser()
    config.read("db.cfg")

    # Connect to planetscale db
    conn = mysql.connector.connect(
        host = f"{config['DB']['HOST']}",
        port = int(f"{config['DB']['DB_PORT']}"),
        user = f"{config['DB']['DB_USER']}",
        password = f"{config['DB']['DB_PASSWORD']}",
        db = f"{config['DB']['DB_NAME']}",
        ssl_verify_identity = True,
        ssl_ca = f"{config['DB']['SSL_CA']}"
    )
    
    # Create cursor
    cur = conn.cursor()

    for setting in settings_queries:
        cur.execute(setting)
        conn.commit()

    return cur, conn

def test_db():
    """
    Tests db by asking for a list of tables
    """
    try:
        cur, conn = make_connection()
        cur.execute("SHOW TABLES;")
        row = cur.fetchall()
        print(row);
    except mysql.connector.Error as err:
        print(f"Failed to get table info: {err}")
        exit(1)

    # Close connection
    conn.close()


def main():
    '''
    Main ETL function
    '''

    # UNCOMMENT LINES BELOW AS WELL AS process_data() below to repopulate db with records
    # Drop Tables
    # drop_tables()

    # Create Tables
    create_tables()
    test_db()

    # UNCOMMENT LINES BELOW AS WELL AS drop_tables() above to repopulate db with records
    # Process and insert clearscore data
    # process_data(filepath = 'data/raw/credit_reports', func = process_credit_reports_data)
    # process_data(filepath = 'data/raw/logins', func = process_logins_data)
    # process_data(filepath = 'data/raw/card_clicks', func = process_card_clicks_data)

    ## Download data
    # download_data(credit_reports_with_conversion_data, ['masked_id', "local_datetime", "local_date", "credit_score", "employment_status", "residential_status", "salary", "ever_default", "ever_delinquent", "birth_date", "months_since_default", "open_credit_cards", "open_loans", "converted", "converted_date"], 'data/processed/credit_reports_with_conversion_data.csv')
    


if __name__ == "__main__":
    main()
