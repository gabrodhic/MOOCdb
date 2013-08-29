'''
Created on Jun 15, 2013
@author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''


def main():
    '''
    This is the main function
    '''
    file = open("user_certifcate_per_country_normalized_cutoff100_2_columns.csv", 'r')
    file_output = open("user_certifcate_per_country_normalized_cutoff100_2_columns.data", 'w')
    
    count = 0
    for cur_line in file:
        count  += 1
        if count <= 1:
            continue
        line = cur_line.split(",")
        output = "['" + line[0] + "',"
        output += line[1].replace("\n", "") + "],\n"      
        file_output.write(output)
        
    file.close()
    file_output.close()

if __name__ == "__main__":
    main()