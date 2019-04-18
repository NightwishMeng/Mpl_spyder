import re
import pymongo
import pandas
import traceback
import pprint
import shutil

"""
String related function

"""
def validatetitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def dropsuffix(string):
	return string[:string.find('.')]
"""
DateBase Related function

"""

#Connect to datebase by name
def connect_db(website_name,datebase_name = '开放数据平台'):
	client = pymongo.MongoClient('mongodb://localhost:27017/')
	db = client[datebase_name]
	collection = db[website_name]
	print('Finish Connect to database: ',datebase_name,' collection:',website_name)
	return collection

#利用pandas去重,默认返回去重后的dict
def drop_duplicated(collection,keyword='_id',coverOrign=False):

	records = collection.find()
	print("Start drop_duplicated: the origin records count: ",records.count())

	dataframe = pandas.DataFrame(list(records))
	dataframe = dataframe.drop_duplicates(keyword,'first')
	datas = dataframe.T.to_dict()

	if coverOrign is True:
		collection.delete_many()
		for data in datas:
			# print(datas[data])
			collection.insert(datas[data])
		# result = collection.find()
		# print("After the records count: ",result.count())
		# return datas
	print("After the records count: ",len(datas))
	return datas



#将database数据转化为csv
def list_to_csv(collection,deldict=[],path=''):
	print("Start Transform database data to csv file: ")
    records = collection.find()
    dataFrame = pandas.DataFrame(list(records))
    try:
    	for word in deldict:
        	del dataFrame[word]
    except Exception as e:
        traceback.print_exc()

    dataFrame.rename(index=str).to_csv(path+
        website_name + '.csv', encoding='utf-8-sig', index=False)

#打印输出database的数据，可根据limlinum控制数据
def datalist(collection,limitnum=0):
	if limitnum is 0:
		records = collection.find()
	else:
		records = collection.find({}).limit(limitnum)

	print("Total num is : ")
	pprint(records.count())
	for record in records:
		pprint(record)


"""
Os related function

"""

#用于删除下载失败为空的文件夹
def getFileSize(filePath):
     
    for root, dirs, files in os.walk(filePath):
    	smsize = 0 
    	for f in files:
    		smsize += os.path.getsize(os.path.join(root, f))
    	if smsize is 0:
    		if root is not path:
    			print("Remove dir:",root)
    			shutil.rmtree(root)


