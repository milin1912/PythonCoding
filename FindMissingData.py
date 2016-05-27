
import glob

import os.path1													# how to reach at actual path of directory

script_dir = os.path.dirname(os.path.realpath('__file__'))		 # fatch the root folder of the file
path1 = os.path.join(script_dir[0:-3],'results/MissingData.out') # Open a folder in file where output will be stored

path = os.path.join(script_dir[0:-3],'data2')					 # given folder with number of files to find missing data in file

currentFile = glob.glob(os.path.join(path, '*.txt'))			
currentFile.sort(key=lambda f: int(filter(str.isdigit, f)))
openfile1 = open(path1, 'w')

for file in currentFile:
    x = file.split('/')[-1]
    with open(file, 'rb') as openfile:
        lines = openfile.read().splitlines()
        row_sets = [[c for c in line.split()] for line in lines]   # List comprehension 
        count=0
        for row in row_sets:
            if row[3] == '-9999':
                count += 1
        openfile1.write(x.strip()+'\t'+str(count)+'\n') 		# Write the missing data back to the file