import numpy as np
import networkx as nx
import json
import n2v.n2v_main as n2v

def load_as_vector():
    path = './emb/authors.emb'
    dict_embvector = {}
    with open(path, 'r', encoding = 'utf-8') as f:
        i = 0
        for line in f:
            if i == 0:
                i = 1
                continue
            tem = line.strip().split(' ')
            dict_embvector[tem[0]] = np.array(tem[1:])
    
    return dict_embvector
            
def cosine_similarity(u, v):
    u = np.array(u, dtype=float)
    v = np.array(v, dtype=float)
    dist = 1 - (u.dot(v) / np.sqrt(u.dot(u)*v.dot(v)))
    return 1 - dist
    
def preprocess():
    path = './graph/authors.edgelist'
    G = nx.read_edgelist(path, create_using=nx.DiGraph())
    nodes = G.nodes(data=False)
    dict_ref = {}
    
    for node in nodes:
        dict_ref[node] = G.predecessors(node)
    
    path2 = 'dict_author2weight.json'
    with open(path2, 'r', encoding = 'utf-8') as f:
        dict_weight = json.load(f)
    
    path3 = 'dict_name2id.json'
    with open(path3, 'r', encoding = 'utf-8') as f:
        dict_name2id = json.load(f)
    
    dict_id2weight = {}
    for each in dict_name2id:
        dict_id2weight[str(dict_name2id[each])] = dict_weight[each]
    
    with open('dict_id2weight.json', 'w', encoding = 'utf-8') as g:
        output = json.dumps(dict_id2weight, indent = 4)
        g.write(output)
        
    print("preprocess done")
    return dict_id2weight, dict_ref, dict_name2id
    
def compute(dict_ref, dict_id2weight, embedding):
    
    for each in dict_ref:
        for predecessor in dict_ref[each]:
            dict_id2weight[each] += cosine_similarity(embedding[each], embedding[predecessor])*\
            dict_id2weight[predecessor] * 0.05  #set a threhold 

    return dict_id2weight

def id2name(dict_id2weight, dict_name2id):
    path = 'dict_author2weight_enhanced.json'
    dict_author2weight_enhanced = {}
    for each in dict_name2id:
        dict_author2weight_enhanced[each] = dict_id2weight[str(dict_name2id[each])]
    
    with open(path, 'w', encoding = 'utf-8') as f:
        json.dump(dict_author2weight_enhanced, f)
        
    print('done')

if __name__ == "__main__":
    embedding = load_as_vector()
    dict_id2weight, dict_ref, dict_name2id = preprocess()
    result = compute(dict_ref, dict_id2weight, embedding)
    
    path = 'dict_id2weight_enhanced.json'
    with open(path, 'w', encoding = 'utf-8') as f:
        json.dump(result, f)
    id2name(result, dict_name2id)
    print('done')
    