import networkx as nx
import numpy as np
from db_utils import *
from db_utils import DataBase
from pymongo import MongoClient
import json
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# output: relation_dict {author_name : [author_name, author_name, ..., author_name]}
def get_nodes_relation(coll):
    nodes = get_db_authors(coll, 1000)
    relation_dict = {}
    
    for node in nodes:
        linked_nodes = get_author_link(coll, node)
        # 仅要目标前1k篇论文的作者
        linked_nodes = [x for x in linked_nodes if x in nodes]
        relation_dict[node] = linked_nodes

    return relation_dict, nodes

# Input: nodes ["a", "b", ...], realtion_dict {"author":['author', '', ...], ...}
# Output: Graph
def generate_graph(nodes, relation_dict, directed = True):
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    G.add_nodes_from(nodes)
    edges = []
    
    for each in relation_dict.keys():
        for tem in relation_dict[each]:
            edges.append((each, tem))
    
    G.add_edges_from(edges)
    
    return G

def save_relation_dict(dic, path = "dict_author_relation.json"):
    with open(path, 'w') as f:
        output = json.dumps(dic, indent=4)
        f.write(output)

def load_relation_dict(path = "dict_author_relation.json"):
    with open(path, 'r') as f:
        dic = json.load(f)
    
    return dic

def name2id(relation_dict, path = "dict_name2id.json", w = False):
    dict_name2id = {}
    i = 1
    for tem1 in relation_dict:
        if tem1 in dict_name2id:
            continue
        else:
            dict_name2id[tem1] = i
            i += 1 
    
    if w:
        with open(path, 'w') as f:
            output = json.dumps(dict_name2id)
            f.write(output)
        print("name2id write to local..")
            
    return dict_name2id

def name2id_relation2dict(relation_dict, dict_name2id):
    
    dict_final = {}
    for each in relation_dict:
        tem_to = []
        for tem in relation_dict[each]:
            try:
                tem_to.append(dict_name2id[tem])
            except Exception:
                print("key error")
        dict_final[dict_name2id[each]] = tem_to
    
    return dict_final
            
    

def graph(G, path = "com_G_labels.png"):
    nx.draw(G, with_labels = False, node_size = 20)
    plt.savefig(path)

if __name__ == "__main__":
    aminer = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
    coll = aminer.collection
    start_time = time.time()
    
    dict_author2author, nodes = get_nodes_relation(coll)
    # print(len(nodes))
    # print(len(dict_author2author))
    # 获取name和数字编号的映射
    dict_name2id = name2id(dict_author2author, path = 'dict_name2id.json', w = False)
    # 获取数字编号的作者引用关系字典
    dict_relaition_numeric = name2id_relation2dict(dict_author2author, dict_name2id)
    # save_relation_dict(dict_relaition_numeric, path = "dict_author_relaition_numeric.json")
    G = generate_graph(nodes, dict_relaition_numeric)
    # nx.write_edgelist(G, './graph/authors.edgelist')
    
    # nx.write_edgelist(G, './graph/test_authors.edgelist')
    # nodes = get_db_authors(coll, 1000)
    # relation_dict = load_relation_dict()
    G = generate_graph(nodes, dict_relaition_numeric)
    end_time = time.time()
    print(str((end_time-start_time)/3600) + ' hours')
    graph(G)
    print("Done!")
    # print(dic)
    