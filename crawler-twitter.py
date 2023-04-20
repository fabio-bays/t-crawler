import os
import json

from databases.src.postgresql import postgres_db
from credentials import *
from crawler.src.twitter_api_scrap import twitter_api_scrap

def warp(twitter_credentials, postgres_credentials):
    pgdb = postgres_db(postgres_credentials)
    twitter_api_scrap(twitter_credentials, pgdb)
    
def main():
    twitter_credentials_list=[]
    postgres_credentials_list=[]

    path_home = os.path.dirname(os.path.realpath(__file__)) + '/crawler'   
    setup_file=(path_home + '/setup.json')   
    
    with open(setup_file, "r") as setup_file:  
        data_setup = json.load(setup_file)       
        
        #  For each connection in the setup file, save the credentials information
        for connections in data_setup['twitter_connections']:     
            twitter_credentials_list.append(twitter_credentials(connections['user'],
                                                connections['consumer_key'],
                                                connections['consumer_secret'],
                                                connections['bearer_token'],
                                                connections['access_token'],
                                                connections['access_token_secret'],
                                                connections['filter_rules']))  

        for postgres_connection in data_setup['postgres_connections']:
            postgres_credentials_list.append(postgres_credentials(
                                                user=postgres_connection['user'],
                                                host=postgres_connection['host'],
                                                password=postgres_connection['password'],
                                                database=postgres_connection['database']))
    
    # Just one twitter api connection will be used, for now
    warp(twitter_credentials=twitter_credentials_list[0], 
         postgres_credentials=postgres_credentials_list)
 
if __name__ == '__main__':
    main()