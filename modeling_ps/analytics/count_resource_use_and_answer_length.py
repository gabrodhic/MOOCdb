"""
    Elaind Han (skewlight@gmail.com)
    created 5/4/2014

    This scripts count the number of times each resource is used by all students for particular
    problems. It also finds the distribution of number of attempts per user for each problem.
    1) Save distribution of answer length (number of attempts) per user for all problems in
       "answer_length_distribution.csv" in format:

       Each problem correspond to 2 rows in .csv:
       First row: problem id, 0, 1, 2, 3 ..... representing number of attempts except 0 (see second row)
       Second row: problem id, total number of students who have attempted, count for 1,
                   count for 2, count for 3 ....
    2) Plot resource use counts.
    3) Generate one csv per problem listing resources used ordered from most count to least in format:
       resource id, count, resource_url
       
"""
import csv
import os
from os import listdir
from os.path import isfile, join
import pylab as pl
import math

CSV_FOLDER_PATH = "problem_csv_v2/"
COUNT_FOLDER_PATH = "problem_resource_count/"

USER_INDEX = 0
ANSWER_INDEX = -1
RESOURCE_INDEX = 2
EMPTY_ANSWER = 0
FILE_NAME = "problem_%i_v2.csv"
    
def count_resource_use_and_answer_length(problem_id):

    filename = os.path.join(CSV_FOLDER_PATH, FILE_NAME%problem_id)

    count = {}

    total_lines = 0
    with open(filename,'r') as csvfile:
        reader = csv.reader(csvfile)

        user = None
        user_count = 0
        subcount = {}
        for row in reader:
            total_lines += 1

            if row[0] != user:
                
                user_count +=1
                
                if user:
                    if usersubcount in subcount:
                        subcount[usersubcount] += 1
                    else:
                        subcount[usersubcount] = 1
                user = row[0]
                usersubcount = 0

                
                
            if float(row[ANSWER_INDEX]) == EMPTY_ANSWER: #is a resource

                resource_id = int(row[RESOURCE_INDEX])
                if resource_id not in count:
                    count[resource_id] = 1
                else:
                    count[resource_id] += 1

            else: #is answer
                usersubcount += 1
        #enter last user
        if usersubcount in subcount:
            subcount[usersubcount] += 1
        else:
            subcount[usersubcount] = 1

    bound = 3
    filtered_count = 0
    for i in count:
        if count[i] > bound:
            filtered_count +=1
            
#### print out per problem stats
            
##    print "Problem %3i, total events: %6i, users: %5i, unique: %3i, more than %i counts: %i"\
##          %(problem_id,total_lines,user_count,len(count),bound,filtered_count)
##    
##    if 100<= filtered_count and 150>= filtered_count:
##        print "Problem %3i, total users: %5i, longest: %3i, unique length: %3i"\
##              %(problem_id,user_count,max(subcount.keys()),len(subcount))
##        s = ""
##        strr=""
##        strr2=" "
##        for u in sorted(subcount)[:10]:
##            s += "%5i| "%u
##            strr += "%5i| "%subcount[u]
##            strr2 += "%.2f|  "%(float(subcount[u])/user_count)
##        print s
##        print strr
##        print strr2
##        print ""
    return count,filtered_count,user_count,subcount

def load_resources():
    filename = 'resources.csv'
    res = {}

    with open(filename,'r') as csvfile:
        reader = csv.reader(csvfile)
        header = reader.next()
        for row in reader:
            res[int(row[0])] = row[1]
    return res

def create_bins(use,unique,log=False,ordered=False):
    # use = resource_use dictionaries, key: resource_id, value : count
    # unique = list of unique resources, not all might have appeared in use
    
    if ordered:
        bins = []
        labels = []
        l=[(v,k) for k,v in use.iteritems()]
        l.sort(reverse=True)
        for (v,k) in l:
            if log:
                bins.append(math.log(v))
            else:
                bins.append(v)
            labels.append(k)
        for k in unique:
            if k not in labels:
                bins.append(0)
                labels.append(k)
        return bins,labels
        
    else:
        bins = [0]*len(unique)
        for i in range(len(unique)):
            if unique[i] in use:
                if log:
                    bins[i] = math.log(use[unique[i]])
                else:
                    bins[i] = use[unique[i]]

        return bins,unique



if __name__ == "__main__":
    problem_list = []
    pwd = os.getcwd()
    ##### Automatically loads list of student trajectories csv's for all problems
    files = [ f for f in listdir(join(pwd,CSV_FOLDER_PATH)) if isfile(join(pwd,CSV_FOLDER_PATH,f)) ]

    ##### graph options
    log = True #use logged counts
    ordered = False #True = order resources by counts, False = order resources by id 

    fontsize = 24
    
    for f in files:
        problem_list.append(int(f.split('_')[1]))
    problem_list.sort()
    #print total number of problems
    print "total number of problems: %i"%len(problem_list)

    ##### Or manually pick problems
    problem_list = [330]

    ##### load from resources.csv which contains resource id and its corresponding url for the whole course.
    res = load_resources()
    
    ##### file that aggregate distribution of number of answers submitted per user for all problems.
    filename = "answer_length_distribution.csv"
    with open(filename,'w') as csvfile:
        writer = csv.writer(csvfile)
        for problem in problem_list:
            ##### plot resource use
            (count,filtered_count,user_count,subcount) = count_resource_use_and_answer_length(problem)

            [bins,labels] = create_bins(count,sorted(count.keys()),log,ordered)
            
            fig = pl.figure()
            if log:
                sup = "Log Resource Use Count Problem %i"%(problem,)
            else:
                sup ="Resource Use Count Problem %i"%(problem,)
            if ordered:
                sup += " ordered"
            fig.suptitle(sup)
                
            ax=pl.subplot(111)
            ax.bar(range(1,len(bins)+1),bins)
            ax.set_xticks(range(0,len(bins),10))
            ax.set_xticklabels(labels[0:len(bins):10], rotation=75)
            pl.xlim([0,len(bins)+1])
            pl.setp(ax.get_xticklabels(), fontsize=fontsize)
            pl.setp(ax.get_xticklabels(), fontsize=fontsize)
            pl.setp(ax.get_yticklabels(), fontsize=fontsize)
            if log:
                pl.ylim([0,11])
            fig.tight_layout()
            pl.show()
            

            ##### record answer length (number of attempts)
            # distribution in answer_length_distribution.csv
            keys = sorted(subcount.keys())
            writer.writerow([problem,0]+keys)
            writer.writerow([problem,user_count]+[subcount[k] for k in keys])

            ##### For each individual problem, list all resources ordered by use counts
            # from most to least together with the actual resource url (loaded in res)
            # in .csv
            l=[(v,k) for k,v in count.iteritems() ]
            l.sort(reverse=True)
        
            filename = join(COUNT_FOLDER_PATH,"problem_%i_resource_count.csv"%problem)
            with open(filename,'w') as csvfile:
                writer = csv.writer(csvfile)
                for (v,k) in l:
                    writer.writerow([k,v,res[k]])
            
        





