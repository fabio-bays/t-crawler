# t-crawler
t-crawler is a Twitter social media crawler, built on top of Tweepy. With it, Volunteered Geographic Information (VGI), and other useful data, can be gathered, and saved for later analysis. It collects tweet objects and store them in a PostgreSQL database.

### Dependencies
Tweepy 4.12.1 or above.
https://docs.tweepy.org/en/stable/install.html

psycopg2 2.9.5 or above.
https://www.psycopg.org/docs/install.html

### How to setup
Open setup.json and put all the necessary values. 

![Setup file](https://user-images.githubusercontent.com/92861897/233638035-f8985b23-5527-4237-8cc9-b48d7a5c84d6.png)

For `twitter_connections`, only a Twitter API's user bearer token, and filter rules are necessary.

To get a bearer token, you will need a [developer account](https://developer.twitter.com/en/docs/tutorials/step-by-step-guide-to-making-your-first-request-to-the-twitter-api-v2) in Twitter.

Each filter rule is a dictionary json object, nested inside a list of rules. They have the value and tag keys, with their values being strings. A tag key is neccessary, but its value can be left empty. If there are no filter rules, the crawler will not execute. See [how to build a rule](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule). 


For `postgres_connections`, every key needs a value. The values are all of type string. 
To use a public schema, use the value `"public"` for the `schema` key.

### How it works

If there are rules in the setup file, the Twitter API's rule object will be saved on a PostgreSQL database rule table. Then, an attempt of connection with the API's streaming endpoint will be done. If successful, the crawler will start to gather tweet objects, respecting the filter rules.

Rule and tweet objects are json files. Therefore, the database respective tables should have an attribute of type json.
See [rule objects](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream-rules) and
[tweet objects](https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet).

To do a controlled disconnection, a `KeyboardInterrupt` Python exception should happen. Generally, Ctrl+C combination in the terminal does that.
In a controlled disconnection, all the filter rules are removed.

