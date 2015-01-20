from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import yaml


def setup():

    auth_list = []
    setup_file = open("./streaming/twitter/setup.yaml", "r")
    setup_docs = yaml.load_all(setup_file)
    for doc in setup_docs:
        auth_list.append(doc['authentication']['access_token'])
        auth_list.append(doc['authentication']['access_token_secret'])
        auth_list.append(doc['authentication']['consumer_key'])
        auth_list.append(doc['authentication']['consumer_secret'])
        track_list = doc['tracks']

    return auth_list, track_list


class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


def fire():
    auth_list, track_list = setup()

    l = StdOutListener()
    auth = OAuthHandler(auth_list[2], auth_list[3])
    auth.set_access_token(auth_list[0], auth_list[1])
    stream = Stream(auth, l)

    stream.filter(track=track_list)


