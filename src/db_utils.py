import numpy as np 
from pymongo import MongoClient
import re
# read data from mongo db
import sys
import io
# in order to make print work well
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

class DataBase(object):
	# url + user_name + passcode
	def __init__(self, url, db, collection):
		self.url = url
		self.client = MongoClient(url)
		self.db = self.client[db]
		self.collection = self.db[collection]
		print('target url:%s, db:%s, collection:%s ' %(url,db,collection))

# get references of a given id paper 
def get_ref_authors(coll, id):
	paper = coll.find({"id":id})[0]
	authors = []
	# any better suggestion ?
	authors = paper["authors"]
	author_names = []
	for author in authors:
		try:
			author_names.append(author["name"])
		except Exception:
			print("not a dict")
	return author_names

# find all the authors that the given author have been cited
def get_author_link(coll, _name):
	papers = coll.find({"authors":{"$elemMatch":{"name":_name}}})
	link_authors = []
	for each in papers:
		try:
			refs = each["references"]
			for ref in refs:
				link_authors.append(get_ref_authors(coll, ref))
		except Exception:
			print("not find ref or paper in collection")
	# get rid of a list 
	link_authors = sum(link_authors, [])
	
	return link_authors

# get some authors from database as our research material
def get_db_authors(coll, limit = 1000):
	authors = coll.find({},{"authors":1}).limit(limit)
	target_authors = []
	for author in authors:
		for each in author["authors"]:
			target_authors.append(each["name"])
			
	return set(target_authors)

# construct the test collection
def transfer_db(coll, coll_new, limit_num = 10000):
	for each in coll.find({}).limit(limit_num):
		coll_new.insert(each)
	
	print("done!")

if __name__ == "__main__":
	aminer = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
	test = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "debug_test")
	coll = aminer.collection
	coll_new = test.collection
	transfer_db(coll, coll_new, 100)
	# a = coll.find({})[0]
	# print(a)
	# authors = get_db_authors(coll)
	# print(authors[0])
	# link = get_author_link(coll, authors[0])
	# print(link)
	