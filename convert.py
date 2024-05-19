import csv
import json

data = json.load(open('data.json', 'r'))

for i in range(len(data)):
    if int(data[i]['BC_D \nGIRLS']) < 10000 :
        print(data[i]['Institute Name'])