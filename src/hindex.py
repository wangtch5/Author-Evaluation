import numpy as np
import datetime
from db_utils import *
import json
from stat_utils import *

def h_index(dic):
    dict_h_index = {}
    for each in dic:
        temp = dic[each]
        # sorted by n_citation
        temp = sorted(temp, key = lambda x: x[1], reverse = True)
        i = 0
        h = 0
        for i in range(len(temp)):
            h = temp[i][1]
            if h <= i + 1:
                break
            else: h = i + 1 
        
        dict_h_index[each] = h
    
    return dict_h_index
    

# Output: dict_author2paper {"name":[(id, citations),...]}
def author2papers(coll, authors):
    dict_author2paper = {}
    for name in authors:
        papers = coll.find({"authors":{"$elemMatch":{"name":name}}})
        paper_id = []
        for each in papers:
            try:
                paper_id.append((each["id"], each["n_citation"]))
            except Exception:
                print("no citation number")
        dict_author2paper[name] = paper_id
    
    return dict_author2paper
        

if __name__ == "__main__":
    # test = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "debug_test")
    # coll = test.collection
    aminer = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
    coll = aminer.collection
    # 1000 authors 
    authors = get_db_authors(coll)
    dict_author2paper = author2papers(coll, authors)
    dict_h_index = h_index(dict_author2paper)
    
    # print(dict_h_index)
    # dict_h_index = sort_dict(dict_h_index, True)
    with open("dict_h_index.json", 'w') as f:
        output = json.dumps(dict_h_index, indent = 4)
        f.write(output)