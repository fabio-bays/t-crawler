class twitter_credentials:         
    def __init__(self,user,consumer_key,consumer_secret,bearer_token,
                 access_token,access_token_secret,filter_rules): 
            
        self.user=user
        self.consumer_key = consumer_key
        self.consumer_secret=consumer_secret
        self.bearer_token=bearer_token
        self.access_token=access_token
        self.access_token_secret=access_token_secret
        self.filter_rules=filter_rules

class postgres_credentials:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
    