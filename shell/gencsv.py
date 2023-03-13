import csv
import itertools
import string


filePath = "result.csv"
jobn = ['A', 'B']
matrix = ['thr', 'occ']

lis = []
k=0
for i in matrix:
  for j in jobn:
    with open(i+"_"+j+".txt") as f:
      temp = f.readlines()
      lis.append([ string.atof(x.strip()) for x in temp])
      lis[k].insert(0,i+"_"+j)
    k = k + 1
f.close()

rows = list(itertools.izip_longest(lis[0],lis[1],lis[2],lis[3]))

with open(filePath, "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
