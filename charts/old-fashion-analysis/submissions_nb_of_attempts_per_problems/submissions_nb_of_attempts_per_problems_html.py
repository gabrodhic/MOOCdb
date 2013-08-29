'''
Created on Jun 22, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''


def main():
    '''
    This is the main function
    '''
    file = open("submissions_nb_of_attempts_per_problems.csv", 'r')
    file_output = open("submissions_nb_of_attempts_per_problems.data", 'w')
    
    count = 0
    for cur_line in file:
        count  += 1
        if count <= 1:
            continue
        line = cur_line.split(",")
        output = "['" + str(count-1) + "'," 
        output += line[1].replace("\n", "") + "],\n"      
        file_output.write(output)
        
    file.close()
    file_output.close()

if __name__ == "__main__":
    main()