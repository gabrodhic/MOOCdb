'''
Created on Jun 22, 2013

@author: francky
'''

def main():
    '''
    This is the main function
    '''
    file = open("submissions_per_country.csv", 'r')
    file_output = open("submissions_per_country.data", 'w')
    
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