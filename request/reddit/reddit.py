import urllib2
import json
import time
import datetime
import yaml
from pymongo import MongoClient as MC


def setup():
    setup_file = open("./request/reddit/setup.yaml", "r")
    setup_docs = yaml.load_all(setup_file)

    for doc in setup_docs:
        base_url = doc['base_url']
        limit = doc['default_limit']
        subreddits_list = doc['subreddits']

    urls = []

    for sub in subreddits_list:
        u = base_url % (sub, limit)
        urls.append(u)

    return urls


def mongo_connect():

    client = MC()
    db = client.CTI_IR
    collection = db.reddit

    return client, collection


def mongo_insert(collection, entries):

    for entry in entries:
        collection.insert(entry)


def mongo_disconnect(client):

    client.close()


def download(url):
    try:
        response = urllib2.urlopen(url)
    except:
        response = "Could not retrieve resourse"

    return response


def parse_json(response):

    jinput = json.loads(response.read())
    entries = []

    for i in jinput["data"]["children"]:
        url = i["data"]["url"]
        title = i["data"]["title"]
        score = i["data"]["score"]
        num_comments = i["data"]["num_comments"]
        ups = i["data"]["ups"]

        entry = {"u": url, "t": title, "sc": score, "nc": num_comments, "up": ups}
        entries.append(entry)

    return entries


def run():

    urls = setup()
    client, collection = mongo_connect()

    responses = []

    for url in urls:
        responses.append(download(url))

    for response in responses:
        entries = parse_json(response)
        mongo_insert(collection, entries)

    mongo_disconnect(client)

    print "Reddit scraping has finished"


def iterate(interval):
    while True:
        run()
        print "Iteration: " + str(datetime.datetime.now())
        time.sleep(interval)
