import os
from os import listdir
from os.path import isdir, join
import re
from data import *
import shutil
from utils import get_classes


if __name__ == '__main__':
    classes = get_classes()
    client = pymongo.MongoClient("localhost", 27017)
    for dir_name, db_name in classes:
        # print db_name
        # if db_name not in ['mitx_6_00x_2013_spring', 'mitx_6_00_1x_2013_3t']:
        #     continue

            
        db = client[db_name]
        m = MongoMOOC(db)   
        try:
            out_dir = "classes/" + dir_name + "/"
            shutil.rmtree(out_dir, ignore_errors=True)
            os.makedirs(out_dir)
        except:
            pass
        # m.db.collaborations.drop()
        # m.import_dump("/data/"+dir_name+"/")
        # edges = m.export_edges(out_dir+db_name)
        # print edges
        
        cmd = "./community_analysis.py --db_name %s --output_csv %s --output_graphs %s --date_interval 21 --num_topics 10 --passes 10" % (db_name, out_dir+db_name, out_dir+db_name)
        print "cmd %s" % (cmd)
        os.system(cmd)