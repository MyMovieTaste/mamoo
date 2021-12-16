import csv
import json

csvFilePath = '../fixtures/year.csv'
jsonFilePath = '../fixtures/year.json'

result = []
with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        year_dict = {
            "model" : "movies.year",
            "id" : row['pk'], 
            "fields" : {
                "year_int" : int(row['pk']),
            }
        }
        
        result.append(year_dict)
        
with open(jsonFilePath, 'w', encoding="UTF-8") as jsonFile:
    jsonFile.write(json.dumps(result, indent=2))
