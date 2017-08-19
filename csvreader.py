import csv
def readCSV(filename):
    dataArray = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            dataArray.append(row)
    csvfile.close()
    return dataArray

def readCSVasDict(filename):
    dataDict = {}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) < 2:
                print("Row only has one value! Try using readCSV().")
                return
            dataDict[row[0]] = row[1:]
    csvfile.close()
    return dataDict
