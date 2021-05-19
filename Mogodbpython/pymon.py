import pymongo 
client = pymongo.MongoClient(host='localhost',port=27017)
#指定資料庫
mydb = client.erictest
#指定資料
collection = mydb.pttstock
# date1 = {'name':'rong','kg':55,'age':24}
#插入
# collection.insert(date1)
#查詢
result = collection.find().sort('_id' , -1).limit(1)
res = collection.find_one()
print(res)
for res in result:
    print(res['_id'])
# if collection.find_one({'name':'rong'}) == None :
#     print(True)
# else :
#     print(False)
