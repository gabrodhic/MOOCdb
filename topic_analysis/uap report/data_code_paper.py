import MySQLdb
import pickle
import pymongo
import json
import random

class MoocData():
    def get_edges():
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
            
class MongoMOOC(MoocData):
    """
    command to load dump
    '/mongodb/bin/mongoimport.exe --db %s --collection %s  --jsonArray < "%s"' % (db, collection, f)
    """
    def __init__(self, db):
        self.db = db
    def get_edges(self, start_date='2012-03-04 16:57:49', end_date='2012-03-06 16:57:49'):
        graph = self.db.collaborations.aggregate([
        {
            '$match' : {
                'parent_ids' : {
                    '$not' : { '$size' : 0 }
                }
            }
        },
        {
            '$unwind' : "$parent_ids"   
        },
        {
            '$group' : {
                '_id':"$author_id",
                'neighbors' : {
                    '$push': "$parent_ids"
                }
            }
        }])

        result = []
        for node in graph['result']:
            neighbors = db.collaborations.aggregate([
                {
                    '$match' : {
                        "_id" : {
                            '$in' : node['neighbors']
                        }
                    }
                },
                {
                    '$group' : {
                        "_id" : "$author_id",
                        "weight" : {
                            '$sum' : 1
                        }
                    }
                }

            ])

            for neighbor in neighbors["result"]:
                edge = (int(node["_id"]), int(neighbor['_id']), neighbor['weight'])
                result.append(edge)

        return result

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
