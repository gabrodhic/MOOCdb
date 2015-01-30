import MySQLdb
import pickle
import pymongo
import json
import random
import os
from os import listdir
import logging, gensim, bz2
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pdb
from collections import Counter
from topics import *
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
class MoocData():
    def get_edges():
        raise NotImplementedError

    def get_first_last_date(self):
        raise NotImplementedError

    def anon_rows(self, rows):
        """
        rows ---> rows of edges list
        """

        mapping = {} #real id to "fake" id
        new_rows = []
        for r in rows:
            if r[0] not in mapping:
                mapping[r[0]] = random.randint(0,1000000)
            
            if r[1] not in mapping:
                mapping[r[1]] = random.randint(0,1000000)

            new_row = ( mapping[r[0]], mapping[r[1]], r[2] )
            new_rows.append(new_row)

        return new_rows, mapping

    def export_edges(self,f):
        rows = self.get_edges()
        rows, mapping = self.anon_rows(rows)

        with open(f+"_mapping", 'w') as out:
            out.write(json.dumps(mapping))
        
        with open(f+"_edges", 'w') as out:
            for r in rows:
                out.write( "%d,%d,%d\n" % (r[0], r[1], r[2]) )

        return f+"_edges" 




class MockMOOC(MoocData):
    """
    Mock datasource. Takes a file name. look at mock_data.csv for example
    """
    def __init__(self, f):
        self.f = f

    def get_edges(self):
        edges = []
        with open(self.f, "r") as edges:
            edges = [e.split(",") for e in edges]
            return [(int(e[0]), int(e[1]), int(e[2])) for e in edges]
            

class MySQLMOOC(MoocData):
    def __init__(self, db=None, mock=True):
        self.mock=mock
        try:
            mysql = db #MySQLdb.connect(host="localhost",user="root", passwd="edx2013", db="fall2012_moocdb", port=3316)
            self.cur = mysql.cursor()
        except:
            self.mock=True

        if self.mock:
            print "Using mockdata"
    
    def get_edges(self):
        query = """
        SELECT child.user_id, parent.user_id,  count(*)
        FROM moocdb.collaborations  child
        JOIN moocdb.collaborations parent
        ON parent.collaboration_id=child.collaboration_parent_id
        GROUP BY child.user_id, parent.user_id;
        """
        #TODO: implement start_date and end_date
        self.cur.execute(query, (start_date, end_date))
        rows = self.cur.fetchall()
        with open("mock/rows", "w") as f:
            pickle.dump(rows, f)
            
        return rows

class MongoMOOC(MoocData):
    def __init__(self, db):
        # self.client = pymongo.MongoClient("localhost", 27017)
        # db = self.client.fall2012
        self.db = db
        self.name = db.name

    def import_dump(self, dump_folder):
        dump_folder += "csv_data/"
        print dump_folder
        print "dump_folder %s" %(dump_folder)
        f = [x for x in listdir(dump_folder) if "forum" in x][0]
        
        if not f:
            raise "No forum file"

        print "file: %s" % (dump_folder+f)


        cmd = "mongoimport --file %s  --db %s --collection collaborations" % (dump_folder+f, self.db.name)
        print "cmd %s" % (cmd)
        os.system(cmd)
        count = 0
        for u in self.db.collaborations.find({"_type":"CommentThread"}).batch_size(1000):
            count += 1
            print count, u["_id"]

            self.db.collaborations.update({"comment_thread_id": u["_id"]}, {'$push' : {"parent_ids":u["_id"]}}, multi=True)
            self.db.collaborations.update({"comment_thread_id": u["_id"], 'parent_id': None}, {'$set' : {"parent_id":u["_id"]}}, multi=True)

            u['comment_thread_id'] = u["_id"]
            self.db.collaborations.save(u)


        print "%s threads updated" % count


    def get_first_last_date(self):
        first = self.db.collaborations.find().sort("created_at", 1)[0]["created_at"]
        last  = self.db.collaborations.find().sort("created_at", -1)[0]["created_at"]
        return first, last

    def get_num_students(self):
        return len(self.db.collaborations.distinct("author_username"))

    def get_num_posts(self,start=None, end=None):
        created_at = {"$exists": 1}
        if start and end:
            created_at = {"$gte": start, "$lt": end}
        return self.db.collaborations.find({"created_at":created_at}).count()

    def num_threads_no_reply(self, start=None, end=None):
        created_at = {"$exists": 1}
        if start and end:
            created_at = {"$gte": start, "$lt": end}
        replied = set(self.db.collaborations.find({"_type": "Comment", "created_at":created_at}).distinct("comment_thread_id"))
        threads = set(self.db.collaborations.find({"_type": "CommentThread", "created_at":created_at}).distinct("_id"))
        return len(threads - replied)

    def get_student_posts(self, start=None, end=None):
        created_at = {"$exists": 1}
        if start and end:
            created_at = {"$gte": start, "$lt": end}

        graph = self.db.collaborations.aggregate([
        {
            '$match' : {
                "created_at" : created_at
            }
        },
        {
            '$group' : {
                '_id': {"author_username" : "$author_username", "type":"$_type"},
                'num_posts' : {
                    '$sum': 1
                }
            }
        }])

        posts = {}

        for stud in graph['result']:
            author = stud["_id"]["author_username"]
            post_type = stud["_id"]["type"]

            if author not in posts:
                posts[author] = {}
                
            posts[author][post_type] = stud["num_posts"]

        return posts

    def get_edges(self, start=None, end=None):
        created_at = {"$exists": 1}
        if start and end:
            created_at = {"$gte": start, "$lt": end}

        graph = self.db.collaborations.aggregate([
        {
            '$match' : {
                "parent_id" : {"$exists": 1},
                "created_at" : created_at
            }
        },
        # {
        #     '$unwind' : "$parent_ids"   
        # },
        {
            '$group' : {
                '_id':"$author_username",
                'neighbors' : {
                    '$push': "$parent_id"
                }
            }
        }])

            
        result = []
        for node in graph['result']:
            
            neighbor_posts = self.db.collaborations.aggregate([
                {
                    '$match' : {
                        "_id" : {
                            '$in' : node['neighbors']
                        }
                    }
                },
                {
                    '$group' : {
                        "_id" : {"author":"$author_username", "post_id":"$_id"}
                    }
                }

            ])

            post_counts = Counter(node['neighbors'])
            weights = {}
            for neighbor in neighbor_posts["result"]:
                author = neighbor["_id"]["author"]
                post_id = neighbor["_id"]["post_id"]
                if author not in weights:
                    weights[author] = 0

                weights[author] += post_counts[post_id]



            for neighbor in neighbor_posts["result"]:
                author = neighbor["_id"]["author"]
                edge = (node["_id"], author, weights[author])
                result.append(edge)

        return result


    def get_thread_text(self, author_usernames=None, start=None, end=None):
        """
        makes a list of document where each document is the text posted in one thread
        """

        # pdb.set_trace()

        created_at = {"$exists": 1}
        if start and end:
            created_at = {"$gte": start, "$lt": end}

        
        if author_usernames == None:
            author_usernames = {"$exists": 1}
        else:
            author_usernames = {'$in' : author_usernames}



        thread_ids = self.db.collaborations.find({"created_at" : created_at, 'author_username' : author_usernames}).distinct("comment_thread_id")
        
        # if author_username != {"$exists": 1}:
        #     print 'threads', thread_ids, {"created_at" : created_at, 'author_username' : author_username}

        t = self.db.collaborations.aggregate([
            {
            '$match' : {
                'comment_thread_id' : {
                    '$in' : thread_ids
                }
            }
            },
            {"$sort":{"created_at":1}},
            {
                '$group' : {
                    '_id':"$comment_thread_id",
                    'text' : {
                        '$push': "$body"
                    },
                 #    'start' : {
                 #        '$max' : 
                 #    }
                  }
            },
            { '$out' : "agg_temp" }
            ])["result"]

        
        agg = self.db.agg_temp.find()

    
        t = [' '.join(t_i["text"]).encode('utf-8') for t_i in agg]

        return t



