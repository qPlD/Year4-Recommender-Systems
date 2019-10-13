'''
This program will convert a CSV file to a text file.
The main purpose is to re-use the Movielens dataset and visualise it using
a graph and the tSNE software.

Quentin Deligny
'''

from pathlib import Path
from spotlight.validator import Validator
import csv

'''
data_folder = Path("ml-latest-small/")
csv_file1 = "ml-latest-small/ratings.csv"
#csv_file2 = raw_input('Enter the name of your input file: ')
#txt_file = "movielens_ratings.txt"

txt_file = "ml-latest-small/movielens_ratings.txt"
i=0
with open(txt_file, "w") as my_output_file:
    with open(csv_file1, "r") as my_input_file:
        i+=1
        print(i)
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()
'''
csv_file = "ml-latest-small/ratings.csv"
txt_file = "movielens_ratings.txt"

try:
    my_input_file = open(csv_file, "r")
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))

if not my_input_file.closed:
    text_list = [];
    for line in my_input_file.readlines():
        line = line.split(",", 2)
        text_list.append(" ".join(line))
    my_input_file.close()

try:
    my_output_file = open(txt_file, "w")
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))

if not my_output_file.closed:
    #my_output_file.write("double({},{})\n".format(len(text_list), 2))
    for line in text_list:
        separator = ','
        line = line.split(separator, 1)[0]
        my_output_file.write("  " + line + '\n')
    print('File Successfully written.')
    my_output_file.close()
