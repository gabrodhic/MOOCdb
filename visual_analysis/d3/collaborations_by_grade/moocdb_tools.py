import MySQLdb as mdb
import csv

def connect_to_moocdb():
  """
  connect_to_moocdb:

  args: nothing
  returns: a MySQLdb connection object for a local instance of moocdb

  """
  return mdb.connect('127.0.0.1', '', '', 'moocdb', port=3316, charset='utf8')



def read_csv(filename):
  """
  read_csv:

  args: the filename to be read (string)
  returns: a list of the rows of the csv file, where
          each row is represented as another list of 
          the row's elements as strings.
  """

  with open(filename) as f:
    lines = f.readlines()
  del lines[0]

  rows = []
  for line in lines:
    rows.append(line.split(','))

  return rows



def counter_dict(types):
  """
  counter_dict:

  args: a list of strings declaring the types of the dictionary
  returns: a dictionary mapping each of the types to 0
  """

  temp_dict = {}
  for type1 in types:
    temp_dict[type1] = 0
  return temp_dict