_author__ = 'nick'

import sys
import getopt
import imp
import threading
import yaml
import time


class Agent(object):
    def __init__(self, mid, name, description, interval):
        self.mid = mid
        self.name = name
        self.description = description
        self.interval = interval


def load_agents():
    agent_list = []
    agent_file = open("agents.yaml", "r")
    agent_docs = yaml.load_all(agent_file)

    for doc in agent_docs:
        a = Agent(doc['Id'], doc['Name'], doc['Description'], doc['Interval'])
        agent_list.append(a)

    return agent_list


def load_arguments(agent_list):
    long_arguments = []

    for agent in agent_list:
        long_arguments.append(agent.mid+"=")

    return long_arguments


def main(argv):

    agent_list = load_agents()
    long_arguments = load_arguments(agent_list)

    run = {}

    for agent in agent_list:
        run[agent.mid] = agent.interval

    try:
        opts, args = getopt.getopt(argv, "h", long_arguments)

    except getopt.GetoptError:
        print 'not using it right'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'that is how you use it'
            sys.exit()
        else:
            run[opt.replace('--', '')] = int(arg)

    for k in run:
        if run[k] < 0:
            print k + " won't run"
        elif run[k] == 0:
            print k + " will run just once"
            f = k + "/" + k + ".py"
            func = imp.load_source(k, f)
            t = threading.Thread(target=func.run, args=[])
            t.start()
        else:
            print k + " will run every " + str(run[k]) + " minutes"
            f = k + "/" + k + ".py"
            func = imp.load_source(k, f)
            t = threading.Thread(target=func.iterate, args=[run[k]*60])
            t.daemon = True
            t.start()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1:])

