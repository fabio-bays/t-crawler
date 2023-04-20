import tweepy
import logging
import json
from sys import exit

logging.basicConfig(filename='log.txt',filemode='w',level=logging.DEBUG,
                    datefmt='%c', format='At %(filename)s: %(asctime)s:' \
                    '%(levelname)s:%(name)s: %(message)s\n')

class twitter_api_scrap():          
    def __init__(self,credential,pgdb):
        self.init(credential,pgdb)                     
   
    def init(self,credential,pgdb):
        try:        
            my_stream = MyStream(bearer_token=credential.bearer_token,
                                 postgresdb=pgdb)

            #  Rules should be added before the filter.
            #  If there are rules in the setup, overwrite the existing ones 
            #  and start crawling;
            #  If there is not any rule in the setup, quit the program.
            if credential.filter_rules:
                for rule in credential.filter_rules:
                    my_stream.add_rules(tweepy.StreamRule(value=rule["value"],
                                        tag=rule["tag"]))
            
                rule_dict_data = my_stream.get_rules()._asdict()
                pgdb.save_rule(rule_dict_data)

                my_stream.filter(expansions=['geo.place_id', 'author_id'], 
                                 place_fields=['full_name','id',
                                                'contained_within','country',
                                                'country_code','geo','name',
                                                'place_type'])
            else:
                logging.info('No filter rules in the setup file. Exiting...')
                exit()

        except Exception as e:
            if(e == KeyboardInterrupt):
                # Keyboard interrupting (CTRL+C) will cause a controlled disconnection.
                # In a controlled disconnection, the client disconnects from 
                # the stream and all the rules in the api endpoints are removed.
                logging.info('Controlled disconnection. Disconnecting...')
                my_stream.disconnect()
            else: 
                logging.error(e)           
        
  
class MyStream(tweepy.StreamingClient):
    def __init__(self,bearer_token,postgresdb):
        super().__init__(bearer_token)   
        self.pgdb = postgresdb

    def on_data(self, raw_data):
        super().on_data(raw_data)
        self.save_data(raw_data)

    def save_data(self,raw_data):
        tweet_dict_data = json.loads(raw_data)
        self.pgdb.save_tweet(tweet_dict_data)

    def disconnect(self):
        super().disconnect()
        self.on_disconnect() 

    def on_disconnect(self):
        logging.info('Disconnected. Removing rules...')
        rules_list = list(self.get_rules())
        self.delete_rules(rules_list[0])

        

              
        
      
    