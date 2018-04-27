import numpy as np
import pandas as pd
import json

def load_dict(path1, path2):
    with open(path1, 'r', encoding = 'utf-8') as f1:
        dict1 = json.load(f1)
    
    with open(path2, 'r', encoding = 'utf-8') as f2:
        dict2 = json.load(f2)
    return dict1, dict2

def sort_as1(dic1, dic2):
    l1 = []
    l2 = []
    for each in dic1:
        l1.append(dic1[each])
        l2.append(dic2[each])
    
    return l1, l2

def compute_correction(dict1, dict2):
    l1, l2 = sort_as1(dict1, dict2)
        
    ser1 = pd.Series(l1)
    ser2 = pd.Series(l2)
    
    corr = ser1.corr(ser2)
    
    return corr

def show_top10(dic):
    tup = sorted(dic.items(), key = lambda x: x[1], reverse = True)
    names = []
    for each in tup:
        names.append(each[0])
    
    print(names[:10])
    # return names

if __name__ == '__main__':
    path1 = './dict_author2weight_enhanced.json'
    path2 = './dict_h_index.json'
    dic1, dic2 = load_dict(path1, path2)
    corr = compute_correction(dic1, dic2)
    print(corr)
    
    show_top10(dic1)
    show_top10(dic2)
    
    