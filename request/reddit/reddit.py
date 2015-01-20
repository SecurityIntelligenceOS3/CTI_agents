import urllib2
import json
import time
import datetime
from pymongo import MongoClient 


def run():

    # connect to MongoDB database
    client = MongoClient()
    db = client['CTI_IR']
    collection = db['reddit']
    
    # connect to the URL
    # reddit api gives a lot of options in retrieving information you want
    # for ex the new 100 posts : http://www.reddit.com/r/blackhat/new.json?sort=new&limit=100
    # or if you want directly get the posts in json format, simply /.json
    # Limit : default: 25, maximum: 100
    response = urllib2.urlopen('http://www.reddit.com/r/blackhat/.json?limit=50')

    # retrieve the json data
    data = json.loads(response.read())

    for i in data["data"]["children"]:
        url = i["data"]["url"]
        title = i["data"]["title"]
        score = i["data"]["score"]
        num_comments = i["data"]["num_comments"]
        ups = i["data"]["ups"]
        # add values to the entry
        entry = {"u": url, "t": title, "sc": score, "nc": num_comments, "up": ups}  # insert the entry in mongoDB
        collection.insert(entry)

    client.close()
    print "Reddit scraping has finished"



def iterate(interval):
    while True:
        run()
        print "Iteration: " + str(datetime.datetime.now())
        time.sleep(interval)
