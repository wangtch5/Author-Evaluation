import numpy as np
from pymongo import MongoClient
from db_utils import *
from time import time
import json
import datetime
# Compute weight of authors by using the method in Co-Author Network

# author_x is a tuple of name and year of publication
def compute_weight_ab(year_a, year_b):
    Wab = 1/(year_a - year_b + 1)

    return Wab

# output: dict_paper_weight {id : weight}
def compute_weight_paper(coll):
    print("compute weight paper")
    papers = coll.find({})
    dict_paper_weight = {}
    i = 0
    for paper in papers:
        Ca = 0
        year_a = paper["year"]
        try:
            refs = paper["references"]
        except Exception:
            refs = []
        for each in refs:
            try:
                tem = coll.find_one({"id":each})
                year_b = tem["year"]
                Ca += compute_weight_ab(year_a, year_b)
            except Exception:
                i += 1
                
        dict_paper_weight[paper["id"]] = Ca

    print("error catch", i)
        
    return dict_paper_weight

# input: get_db_authors return
# output: dict_author2paper {author_name : (paper_id, name_order, number_N)}
def get_author_paper_relation(coll, authors):
    print("get author paper relationship")
    dict_author2paper = {}
    for name in authors:    
        id_and_order_N = []
        papers = coll.find({"authors":{"$elemMatch":{"name":name}}})
        for each in papers:
            each_names = [x["name"] for x in each["authors"]]
            order = each_names.index(name) + 1
            N = len(each["authors"])
            id_and_order_N.append((each["id"], order, N))
        
        dict_author2paper[name] = id_and_order_N
    
    return dict_author2paper


def compute_weight_Sna(Ca, n, N, r = 0.7):
    Sna = ((1 - r) * np.power(r, n - 1)) / (1 - np.power(r, N)) * Ca
    
    return Sna

def compute_weight(dict_author2paper, dict_paper_weight):
    print("compute weight")
    dict_author2weight = {}
    i = 0
    for each in dict_author2paper.keys():
        temp = dict_author2paper[each]
        S = 0.0 
        for tem in temp:
            try:
                paper_id = tem[0]
                Ca = dict_paper_weight[paper_id]
                author_order = tem[1]
                N = tem[2]
                Sna = compute_weight_Sna(Ca, author_order, N)        
            except Exception:
                Sna = 0.0
                # print("no paper id in the dict_paper_weight")
                i += 1
            S += Sna
        dict_author2weight[each] = S
    
    print("not found in dict_paper_weight ", i)
    
    return dict_author2weight

if __name__ == "__main__":
	authors_db = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
	aminer = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
	coll_authors = authors_db.collection
	coll = aminer.collection
	
	start_time = time()
	authors = get_db_authors(coll_authors)
    # authors = get_db_authors(coll_authors, limit=100000)
	dict_paper_weight = compute_weight_paper(coll)
	
	dict_author2paper = get_author_paper_relation(coll, authors)
	
	dict_author2weight = compute_weight(dict_author2paper, dict_paper_weight)
	
# 	dict_author2weight  = sorted(dict_author2weight.items(), key = lambda x: x[1], reverse = True)
	
	end_time = time()
	print("spend " + str(end_time - start_time) + "s")
    
#     # today = datetime.date.today()
	with open("dict_author2weight.json", 'w', encoding = "utf-8") as f:
	    output = json.dumps(dict_author2weight, indent = 4)
	    f.write(output)

	   # for each in dict_author2weight:
	       # f.write(str(each[0]) + ' ' + str(each[1]))
	       # f.write("\n")
