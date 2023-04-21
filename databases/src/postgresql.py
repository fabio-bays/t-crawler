import psycopg2 as pg
import psycopg2.extras

# dict Python objects can then be converted to PostgreSQL json
pg.extensions.register_adapter(dict, psycopg2.extras.Json)

class postgres_db():
    def __init__(self,postgres_credentials):
        self.schema = postgres_credentials[0].schema
        self.tweets_table = postgres_credentials[0].tweets_table
        self.rules_table = postgres_credentials[0].rules_table

        self.SAVE_TWEET_JSON = 'INSERT INTO {sch}.{table} VALUES (%s)' \
            ''.format(sch=self.schema,table=self.tweets_table)
        self.SAVE_RULE_JSON = 'INSERT INTO {sch}.{table} VALUES (%s)' \
            ''.format(sch=self.schema,table=self.rules_table)
        
        self.db_connection = None
        self.dbcursor = None
        
        self.db_connect(postgres_credentials)

    def db_connect(self, postgres_credentials):
        self.dbconnection = pg.connect(host=postgres_credentials[0].host, 
                                    user=postgres_credentials[0].user,
                                    database=postgres_credentials[0].database,
                                    password=postgres_credentials[0].password)
        self.dbcursor = self.dbconnection.cursor()
    
    def save_tweet(self, tweet_dict_data):
        try:
            self.dbcursor.execute(self.SAVE_TWEET_JSON,
                                [psycopg2.extras.Json(tweet_dict_data)])
            self.dbconnection.commit()
        except Exception as exception:
            self.dbconnection.rollback()
            raise exception

    def save_rule(self,filter_rule_dict_data):
        try:
            self.dbcursor.execute(self.SAVE_RULE_JSON,
                                [psycopg2.extras.Json(filter_rule_dict_data)])
            self.dbconnection.commit()
        except Exception as exception:
            self.dbconnection.rollback()
            raise exception