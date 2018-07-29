#Erik Sandberg
'''
Module to read/write CSV files in the following format:
__________________________________________
|   key1    |   key2    |   key3    | ...|
| dict1val1 | dict1val2 | dict1val3 | ...|
| dict2val1 | dict2val2 | dict2val3 | ...|
------------------------------------------
'''
import csv

class SSWriter():
    def __init__(self):
        self.name = "Bob"

    def writeSheet(self,sheetName,listOfObjects, writeHeader=True):
        contentType = type(listOfObjects[0])
        if len(listOfObjects) == 0:
            return
        listOfDicts = []
        for obj in listOfObjects:
            # listOfObjects is sometimes a list of objects, sometimes a list of dicts. Make them uniform by converting the objects to dicts
            # Need to convert the Objects to Dicts so csv can writerows() correctly
            if contentType != dict:
                listOfDicts.append(obj.__dict__)
            if contentType == dict:
                listOfDicts.append(obj)
        with open(sheetName, "w") as f:
            columnNames = listOfDicts[0].keys()
            DW = csv.DictWriter(f, columnNames)
            if writeHeader:
                DW.writeheader() # write columnNames
            DW.writerows(listOfDicts)

    def readSheet(self,sheetName):
        '''
        Reads a CSV file and returns a list of dictionaries
        Each element in the list is a row in the CSV file
        The keys of the dictionary are the column names in the CSV file
        '''
        try:
            listOfDicts = []
            with open(sheetName,"r") as f:
                DR = csv.DictReader(f)
                for row in DR:
                    listOfDicts.append(row)
            return listOfDicts
        except:
            # File didn't exist, so return empty array
            return []
