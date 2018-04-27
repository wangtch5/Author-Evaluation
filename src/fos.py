from db_utils import *
import numpy as np
import datetime
import time
import json
# 统计各作者的fos出现频率


def compute_freq(dict_number):
    total = 0 
    for each in dict_number:
        total += dict_number[each]
    for each in dict_number:
        dict_number[each] /= total
    
    return dict_number

# Output: dict_fos_stat {fos_word: number, ...}, dict_fos_author {author: {fos:number}, ...}
def get_fos_freq(coll):
    papers = coll.find()
    i = 0
    dict_fos_stat = {}
    dict_fos_author = {}
    
    for paper in papers:
        try:
            fos = paper["fos"]
            for each in fos:
                if each in dict_fos_stat.keys():
                    dict_fos_stat[each] += 1 
                else:
                    dict_fos_stat[each] = 1
            
            authors = paper["authors"]
            for each in authors:
                if type(each) is dict:
                    if each["name"] in dict_fos_author.keys():
                        for fos_i in fos:
                            if fos_i in dict_fos_author[each["name"]].keys():
                                dict_fos_author[each["name"]][fos_i] += 1
                            else:
                                dict_fos_author[each["name"]][fos_i] = 1
                    else:
                        dict_fos_author[each["name"]] = {}
                        for fos_i in fos:
                            if fos_i in dict_fos_author[each["name"]].keys():
                                dict_fos_author[each["name"]][fos_i] += 1
                            else:
                                dict_fos_author[each["name"]][fos_i] = 1
                else:
                    print("not an author dict, I will just ignore it")
        except Exception:
            i += 1 
    print("no fos or authors", i)
    
    dict_fos_stat_freq = compute_freq(dict_fos_stat)
    
    for each in dict_fos_author:
        freq_author = compute_freq(dict_fos_author[each])
        dict_fos_author[each] = freq_author
        
    return dict_fos_stat_freq, dict_fos_author

def sort_dict(dic, r = True):
    tem = {}
    dic = sorted(dic.items(), key = lambda x: x[1], reverse = r)
    i = 1
    for each in dic:
        tem[each[0]] = each[1]
        # 取作者的前5个fos
        if  i == 5:
            break
        i += 1
    
    return tem

if __name__ == "__main__":
	aminer = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
	coll = aminer.collection
	dict_fos_stat, dict_fos_author = get_fos_freq(coll)
	
	for each in dict_fos_author:
	    dict_fos_author[each] = sort_dict(dict_fos_author[each])
    
    
	with open("dict_fos_author.json", 'w') as f1:
	    output = json.dumps(dict_fos_author, indent=4)    
	    f1.write(output)
	
# 	dict_fos_stat = sort_dict(dict_fos_stat)
	
# 	with open("dict_fos_stat.json", 'w') as f2:
# 	    output = json.dumps(dict_fos_stat, indent=4)
# 	    f2.write(output)
	
	print("done!")
