'''
Created on Jun 13, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
'''


def main():
    '''
    This is the main function
    '''
    file = open("user_country_distribution.csv", 'r')
    file_output = open("user_country_distribution.html", 'w')
    
    count = 0
    for cur_line in file:
        count  += 1
        if count <= 2:
            continue
        line = cur_line.split(",")
        output = "['" + line[0] + "',"
        output += line[1].replace("\n", "") + "],\n"      
        file_output.write(output)
        
    file.close()
    file_output.close()

if __name__ == "__main__":
    main()