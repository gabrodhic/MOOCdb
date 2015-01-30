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