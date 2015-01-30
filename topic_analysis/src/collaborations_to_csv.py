import pymongo
import argparse
import csv 
import os
fields = ["collaboration_id","user_id","collaboration_type_id","collaboration_timestamp","collaboration_content",
"collaboration_ip","collaboration_os","collaboration_agent","collaboration_parent_id", "collaboration_child_number"]

def import_dump(f, db_name):
    cmd = "mongoimport --file %s  --db %s --collection collaborations" % (f, db.name)
    print "cmd %s" % (cmd)
    os.system(cmd)
    count = 0
    

def process_children(parent_id, ordered_children, writer):
    global COUNT
    
    #defaults
    collaboration_type_id = 1
    collaboration_ip = None
    collaboration_os = None
    collaboration_agent = None

    if len(ordered_children) == 0:
        return

    collaboration_child_number = 0
    for u in ordered_children:
        # print "Processing thread", u["_id"], collaboration_child_number, "count: ", COUNT
        collaboration_id = u["_id"]
        user_id = u["author_id"]
        collaboration_timestamp = u["created_at"]
        collaboration_content = u["body"].encode('utf-8')
        collaboration_type_id = None
        collaboration_child_number += 1
        collaboration_parent_id = parent_id
        writer.writerow([collaboration_id,user_id,collaboration_type_id,collaboration_timestamp,collaboration_content, collaboration_ip,collaboration_os,collaboration_agent,collaboration_parent_id])
        COUNT += 1
        children = [c for c in db.collaborations.find({"parent_id": u["_id"]}).sort("created_at", pymongo.ASCENDING)]
        process_children(collaboration_id, children, writer)

def run(db, mongo_dump, csv_out):
    global COUNT
    import_dump(mongo_dump, db)

    #defaults
    collaboration_type_id = 1
    collaboration_ip = None
    collaboration_os = None
    collaboration_agent = None

    with open(csv_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect="excel")
        writer.writerow(fields)
        for u in db.collaborations.find({"_type":"CommentThread"}).batch_size(5000):
            # print "Processing CommentThread", u["_id"], "count: ", COUNT
            collaboration_id = u["_id"]
            user_id = u["author_id"]
            collaboration_timestamp = u["created_at"]
            collaboration_content = u["body"].encode('utf-8')
            collaboration_parent_id = None
            collaboration_child_number = None
            writer.writerow([collaboration_id,user_id,collaboration_type_id,collaboration_timestamp,collaboration_content, collaboration_ip,collaboration_os,collaboration_agent,collaboration_parent_id])
            COUNT += 1
            children = [c for c in db.collaborations.find({"comment_thread_id": collaboration_id, "parent_id": None}).sort("created_at", pymongo.ASCENDING)]
            process_children(collaboration_id, children, writer)

    #cleanup
    db.connection.drop_database(db.name)


parser = argparse.ArgumentParser(description='Convert mongo collaborations table to csv for MOOCDB')
parser.add_argument('mongo_dump', type=str, help="input")
parser.add_argument('csv_out', type=str, help="output")
args = parser.parse_args()

COUNT = 0
client = pymongo.MongoClient("localhost", 27017)
db_name = "CSV_OUT_TMP"
db = client[db_name]

run(db, args.mongo_dump, args.csv_out)

if COUNT != db.collaborations.find().count():
    raise Exception("Rows exported doesn't match rows in mongo database")

print "Sucessfully exported %d rows" % (COUNT)