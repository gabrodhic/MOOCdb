import os
from os import listdir
from os.path import isdir, join
import re
from data import MongoMOOC
import pymongo
import hashlib
from topics import TopicModel
from datetime import timedelta, datetime


def makeHash(username):
        '''
        Returns a ripemd160 40 char hash of the given name. 

        :param username: name to be hashed
        :type username: String
        :return: hashed equivalent. Calling this function multiple times returns the same string

        :rtype: String
        '''
        #return hashlib.sha224(username).hexdigest()
        oneHash = hashlib.new('ripemd160')
        oneHash.update(username)
        return oneHash.hexdigest()


def get_classes():
    mypath = "/data/"
    classes = [ f for f in listdir(mypath) if isdir(join(mypath,f)) and f[:4] == "mitx"]
    classes = [(c, re.sub(r'[.]|[-]', "_", c))  for c in classes ]
    return classes

def get_class_dbs():
    classes = get_classes()
    client = pymongo.MongoClient("localhost", 27017)
    for dir_name, db_name in classes:
        db = client[db_name]
        yield MongoMOOC(db)   

def get_date_ranges(graph_data, date_interval=None, start_date=None, date_ranges=None):
    """
    make a list of date ranges to consider.

    date_interval is length of the range and the start_date specifies when to start.

    alternatively, date_ranges can specify a file to read in that contains date ranges
    """
    #figure out date ranges to consider
    first, last = graph_data.get_first_last_date()
    date_ranges = []
    if date_interval:
        if start_date:
            first = start = datetime.strptime(start_date, "%Y-%m-%d  %H:%M:%S")

        i = timedelta(days = date_interval)
        while first < last:
            end = min(first + i, last)
            date_ranges.append((first, end))
            first = end
    elif date_ranges:
        with open(date_ranges) as dates:
            for r in dates:
                r = r.split(" ")
                start = datetime.strptime(r[0], "%Y-%m-%d  %H:%M:%S")
                end = datetime.strptime(r[1].rstrip('\n'), "%Y-%m-%d  %H:%M:%S") 
                date_ranges.append((start, end))

    return date_ranges

def make_topic_model(graph_data, num_topics, passes):
    t=graph_data.get_thread_text()
    topic_model = TopicModel(num_topics, passes)
    topic_model.build(t)
    return topic_model

# Using the generator pattern (an iterable)
class all_threads(object):
    def __init__(self):
        self.classes = get_classes()
        self.curr_threads = []
        self.client =  pymongo.MongoClient("localhost", 27017)

    def __iter__(self):
        for dir_name, db_name in self.classes:
            db = self.client[db_name]
            graph_data = MongoMOOC(db)
            curr_threads = graph_data.get_thread_text()
            for thread in curr_threads:
                yield thread


        
      
            