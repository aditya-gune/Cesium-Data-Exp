import csv
from csvreader import *

rawdata = readCSV('avdata-latlong.csv')
processed = []
for i in enumerate(rawdata):
    if i[0] == 0: continue
    rawlat = i[1][2]
    rawlong = i[1][3]
    #print(rawlat, rawlong)
    try:
        flat = float(rawlat[:2]) + (float(rawlat[2:4])/60) + (float(rawlat[4:6])/3600)
        flong = float(rawlong[:3]) + (float(rawlong[3:5])/60) + (float(rawlong[5:7])/3600)
    except ValueError:
        print(rawlat, rawlong, "is not a float")
        
    if rawlat[-1] == 'N':
        flat = 0 - flat

    if rawlong[-1] == 'W':
        flong = 0 - flong

    
    tline = i[1]
    tline[2] = flat
    tline[3] = flong
    processed.append(tline)

with open('avdata-coord-proc.csv', 'w', newline='') as t:
    csvwriter = csv.writer(t)
    for line in processed:
        csvwriter.writerow(line)
