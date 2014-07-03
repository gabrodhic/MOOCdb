"""
Created on: 2/1/2014
Author: Elaine Han (skewlight@gmail.com)

From problem csv files, generate resource distribution
after each answer attempt (first, second ...) for all users

1. list top resource consulted after each attempt ordered by count/percentatge
2. plot/save historgram of the distribution with
    a) normal or log scale count
    b) ordered by resource_id or count

"""


import csv
import os
import pylab as pl
import math

#CSV_FOLDER_PATH = "problem_csv_ORIGINAL_sample/" #old csv files
CSV_FOLDER_PATH = "problem_csv_v2/" #new csv files

# change the constants accordingly for different csv formats
USER_INDEX = 0
ANSWER_INDEX = -1
RESOURCE_INDEX = 2
FILE_NAME = "problem_%i_v2.csv"

EMPTY_ANSWER = 0
CORRECT_ANSWER = 1

def correct_attempt_stats_from_csv(problem_id,attempt_limit=5):
    
    ####################################
    ######### from csv files ###########
    ####################################
    
    filename = os.path.join(CSV_FOLDER_PATH, FILE_NAME%problem_id) 

    with open(filename,'r') as csvfile:
        reader = csv.reader(csvfile)

        
        user_count = 0 #total user count for this problem
        user_id = None #user id we looking at        
        attempt_number = 0 #which attempt we are on
        user_correct = 0 # 0=incorrect, 1=correct, 2=correct to incorrect for current user
        
        attempt_dict = {} #store correct attempt stats

        correct_to_in = 0 #incorrect after correct 
        correct_after_c = 0 # correct after correct

        resource_use_list = [{} for i in range(attempt_limit)] #list of dictionary counting resource use
                                # for each attempt
        unique_resources = []
        
        for row in reader:
            
            if float(row[ANSWER_INDEX]) != EMPTY_ANSWER: # is a submission event              
                
                row_user_id = int(row[USER_INDEX])

                #re-initialize for every new user
                if user_id != row_user_id:
                    user_id = row_user_id
                    attempt_number = 0
                    user_correct = 0
                    user_count += 1

                attempt_number += 1

                # first correct attempt
                if float(row[ANSWER_INDEX]) == CORRECT_ANSWER and user_correct == 0 : 
                    if attempt_number in attempt_dict:
                        attempt_dict[attempt_number] += 1
                    else:
                        attempt_dict[attempt_number] = 1
                    user_correct = 1
                    
                # user submitting incorrect attempt(s) after correct, count once for same user
                elif float(row[ANSWER_INDEX]) != CORRECT_ANSWER and user_correct == 1:
                    correct_to_in += 1
                    user_correct = 2

                # user submitting correct attempt(s) after correct, count once for same user
                elif float(row[ANSWER_INDEX]) == CORRECT_ANSWER and user_correct == 1:
                    correct_after_c += 1

            else: #resource event
                #should not have user change or attempt change
                resource_id = int(row[RESOURCE_INDEX])

                #keep track a unique list of resources
                if resource_id not in unique_resources:
                    unique_resources.append(resource_id)
                    
                if attempt_number <= attempt_limit:
                    
                    if resource_id not in resource_use_list[attempt_number-1]:
                        resource_use_list[attempt_number-1][resource_id] = 1
                    else:
                        resource_use_list[attempt_number-1][resource_id] += 1
    unique_resources.sort()
                
                    
                
                


    return (attempt_dict,correct_to_in,correct_after_c,user_count,resource_use_list,unique_resources)


def topValue(d,top=10,percentage=True,time=False):
    """
        Sorting a dictionary by key and print out top values in readable format
    """

    resList = []
    countList = []
    
    total = sum(d.values())
    if time:
        total /= 3600.0
    
    l=[(v,k) for k,v in d.iteritems() ]
    l.sort(reverse=True)

    
    print "Unique resources %6i, total visits %6i"%(len(l),total)
    
    idList = []
    valueList = []

    #print the results in formatted string
    res = 0
    top = min(top,len(l))
    while res < top:
        idString = "" #resource id
        cString = "" #count or percentage
        for i in range(10):
            
            #string += "%s  |"%l[ans][1]
            idList.append(l[res][1])
            idString += "%6i |"%(l[res][1])
            if percentage:
                cString += "%5.2f%% |"%(l[res][0]/float(total)*100)
                valueList.append("%5.2f%% |"%(l[res][0]/float(total)*100))
            else:
                cString += "%6i |"%(l[res][0])
                valueList.append("%6i |"%(l[res][0]))
            res += 1
            if res == top:
                print idString
                print cString
                print ""
                return idList,valueList

        print idString
        print cString
        print ""

def create_bins(use,unique,log=False,ordered=False):
    """
        from count dictionary, create bins used for plotting histograms
    """
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
    
    problem_list = [330]
    attempt_limit = 8
    show_resource = 10
    log = True
    ordered = True
    saveToFig = False
    
    for problem in problem_list:
        print "Problem ID: %i\n"%problem
        (attempt_dict,correct_to_in,correct_after_c,user_count,resource_use,unique_resources) = correct_attempt_stats_from_csv(problem,attempt_limit)
        #print "Total student count: %i, Incorrect after correct: %i, Correct after correct: %i"%(user_count,correct_to_in,correct_after_c)
        for i in range(1,attempt_limit+1):
            print "Attempt %3i, number of students: %i, %.2f%% out of total"%(i,attempt_dict[i],100*attempt_dict[i]/float(user_count)) #including incorrect
            topValue(resource_use[i-1],show_resource)

##            ###### print (resource id: count) in order for current attempt #######
##            ####################################################################
##            d=resource_use[i-1]
##            l=[(v,k) for k,v in d.iteritems() ]
##            l.sort(reverse=True)
##            print "Attempt %i"%i
##            for (v,k) in l:
##                print "Resource ID %4i, count: %5i"%(k,v)
##            ####################################################################

                
        print "Incorrect: %.2f%%"%(100*(1-(sum(attempt_dict.values())/float(user_count))))

        for i in range(1,attempt_limit+1):
            [bins,labels] = create_bins(resource_use[i-1],unique_resources,log,ordered)
            fig = pl.figure()
            if log:
                fig.suptitle("Log resource count Problem %i resources after attempt %i"%(problem,i))
            else:
                fig.suptitle("Problem %i resources after attempt %i"%(problem,i))
                
            ax=pl.subplot(111)
            ax.bar(range(1,len(bins)+1),bins)
            ax.set_xticks(range(0,len(bins),5))
            ax.set_xticklabels(labels[0:len(bins):5], rotation=75)
            pl.xlim([0,len(bins)+1])
            if log:
                pl.ylim([0,11])
                
            pl.show()
            
            ## save figure to .png
            if saveToFig:
                name = "Problem_%i_log_attempt_%i"%(problem,i)
                if log:
                    name += "_log"
                if ordered:
                    name += "_ordered"
                name += ".png"
                fig.savefig(name)
            
            
            
            

                


                

                
            



















            
            
