import pymongo
import pymongo
import json
client = pymongo.MongoClient(host='localhost',port = 27017)
mydb = client.erictest
collation = mydb.jsontest
with open("C:\\Users\\Tibame_25\\Downloads\\a5a0e856882c7ef98ead61a96d4b7fbb_export.json" , "r") as f:
    data =json.load(f)
    for d in data:
        collation.insert(d)

result = collation.find()
for r in result:
    print(r)