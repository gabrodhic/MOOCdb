#!/usr/bin/env python
import argparse
import graph
import data
import csv
import pymongo 
from topics import TopicModel
from utils import all_threads
import utils
import pickle
import os.path
import os
import figures 
import pdb

def to_csv(objects, prefix):
    with open(prefix + "_" + objects[0].__class__.__name__.lower(), 'a') as csvfile:
        fields = objects[0].get_output_features()
        writer = csv.writer(csvfile, dialect="excel")
        writer.writerow(fields)
        for o in objects:
            vals = o.get_output_values()
            writer.writerow(vals)

parser = argparse.ArgumentParser(description='Do community analysis on MOOC forum data')

parser.add_argument('--date_ranges', help="file with list of date ranges to generate output for")
parser.add_argument('--date_interval', type=int, help="in days, runs analysis at this interval")
parser.add_argument('--start_date', type=str, help="start date in YYYYMMDD")

parser.add_argument('--num_topics', type=int, default=10, help="number of topics")
parser.add_argument('--passes', type=int, default=10, help="number of passes for lda")


parser.add_argument('--output_csv', help="file name")
parser.add_argument('--output_graphs', help="file name")

parser.add_argument('--db_name', help="name of database")

args = parser.parse_args()



client = pymongo.MongoClient("localhost", 27017)
db = client[args.db_name]

# model_fn = "all_class_model"
# if os.path.isfile(model_fn):
#     print "loading in all_class_model"
#     all_class_model = MetaTopicModel.load(model_fn)
# else:
#     print "building all_class_model"
#     t = all_threads()
#     all_class_model = MetaTopicModel(20, 10)
#     all_class_model.build(client, t)
#     all_class_model.save(model_fn)
#     os.unlink("classes/all_class_model_topic")
#     to_csv(all_class_model.get_topics(), "classes/all_class_model")


#start doing class specific stuff
graph_data = data.MongoMOOC(db)

#build class topic model
topic_model = utils.make_topic_model(graph_data, args.num_topics, args.passes) 

#figure out date ranges to consider
date_ranges = utils.get_date_ranges(graph_data, args.date_interval, args.start_date, args.date_ranges)

#build timeline
time = graph.CommunityGraphTime(graph_data, topic_model, date_ranges)


#start saving stuff
if args.output_csv:
    # to_csv(time.get_community_graphs(), args.output_csv)
    # to_csv(time.get_all_communities(), args.output_csv)
    # to_csv(time.get_all_students(), args.output_csv)
    to_csv(time.get_topics(), args.output_csv)
    # to_csv(time.get_meta_topics(), args.output_csv)

if args.output_graphs:
    # figures.topic_timeline(time, args.output_csv, args.output_csv+"topictimeline.png")
    # figures.draw_communities(time.get_full_class(), args.output_csv+"community_graph")
    # figures.get_topic_num_hist(time.get_full_class(), args.output_csv+"topic_num_hist")
    figures.community_topics(time.get_full_class(), args.output_csv+"community_topics")
    # figures.interval_community_topics(time, args.output_csv+"community_topics")