import numpy as np
import datetime
import time
import json
import sys
import io
# in order to make print work well
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def summary(dic, number = False):
    if number == False:
        data = np.array(list(dic.values()))
    else: 
        data = np.array([len(dic[x]) for x in dic])
        print("for {'a':{...}, ...}")
    max_ = np.max(data)
    min_ = np.min(data)
    median_ = np.median(data)
    mean_ = np.mean(data)

    return {"max":max_, "min":min_, "median":median_, "mean":mean_}
    
def sort_dict(dic, reverse = True):
    tem = {}
    dic = sorted(dic.items(), key = lambda x: x[1], reverse = reverse)
    for each in dic:
        tem[each[0]] = each[1]
    
    return tem

    
    
if __name__ == "__main__":
    with open("dict_fos_author.json", 'r') as f:
        dict_fos_author = json.load(f)
    
    with open("dict_fos_stat.json", 'r') as f:
        dict_fos_stat = json.load(f)
    
    summary_stat = summary(dict_fos_stat)    
    print("Summary for stat is ", summary_stat)
    
    summary_authors = summary(dict_fos_author, number = True)
    print("Summary for authos is ", summary_authors)
    
    