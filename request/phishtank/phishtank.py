import json
import urllib2
import time
import os
import datetime
from pymongo import MongoClient as MC


def run():

    key = "f2ff110cbc701a6bad4d40c2886184cc047ed8f0e503bab578a38f682894dbbb"
    db_url = "http://data.phishtank.com/data/%s/online-valid.json" % key

    response = urllib2.urlopen(db_url)  # download db

    # MongoDB connect

    client = MC()
    db = client.CTI_IR 
    collection = db.phishtank

    collection.remove({})  # delete all data
    input = json.loads(response.read())

    # for each entry in file:
    for j in input:
        # parse specific values
        try:
            url = j['url'] #url
            phish_id = j['phish_id'] #phish_id
            ip_address = j['details'][0]['ip_address']  # ip_address
            cidr_block = j['details'][0]['cidr_block']  # cidr_block
            announcing_network = j['details'][0]['announcing_network']  # announcing_network
            submission_time = j['submission_time']  # submission_time
            verification_time = j['verification_time']  # verification_time
            target = j['target']  # target
    
        except:
            pass
            # write to MongoDB
        try:
            entry = {"u": url, "id": phish_id, "ip": ip_address, "cb": cidr_block, "an": announcing_network, "st": submission_time, "vt": verification_time, "t": target}
            collection.insert(entry)
        except:
            pass

    print "Phistank scraping has finished"


def iterate(interval):
    while True:
        run()
        print "Iteration: " + str(datetime.datetime.now())
        time.sleep(interval)


# end