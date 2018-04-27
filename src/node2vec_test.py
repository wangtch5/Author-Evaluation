import n2v.n2v_main as n2v
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import numpy as np
import json
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation

# 测试node2vec训练出来的节点embedding的聚类效果
def run_node2vec():
    args = n2v.parse_args()
    n2v.main(args)
    print(args)
    print("ok")

def load_n2v_model(path = './emb/authors.emb'):
    model = KeyedVectors.load_word2vec_format(path)
    print("node2vec model loaded...")
    
    return model

def check(model, dic):
    id_ = 36
    tem = model.wv.most_similar(str(id_))
    name = list(dic.keys())[list(dic.values()).index(id_)]
    print(name)
    print(tem)

def load_as_matrix(path_emb):
    embedding_matrix = []
    id_order = []
    with open(path_emb, 'r') as f:
        i = 0
        for each in f:
            if i == 0:  
                i = 1    
                continue
            tem = each.strip().split(' ')
            id_order.append(int(tem[0]))
            embedding_matrix.append(np.array(tem[1:]))
    embedding_matrix = np.array(embedding_matrix)
    
    return id_order, embedding_matrix
                    
def kmeans(X, n_cluster=20):
    kmeans_model = KMeans(n_clusters=n_cluster, random_state = 0).fit(X)
    
    return kmeans_model.labels_
    
def ap_cluster(X):
    ap_model = AffinityPropagation().fit(X)
    
    return ap_model.labels_, ap_model.cluster_centers_indices_
    
    
if __name__ == "__main__":
    model = load_n2v_model()
    with open('dict_name2id.json', 'r', encoding = 'utf-8') as f:
        dict_name2id = json.load(f)
    id_order, embedding = load_as_matrix('./emb/test_author.emb')
    labels = kmeans(embedding, n_cluster=7)
    
    # labels, centers = ap_cluster(embedding)
    # print('number of centers', len(centers))
    labels = labels.tolist()
    # output_path = "ap_cluster_result.txt"
    output_path = 'test_kmeans_cluster_result.txt'
    with open(output_path, 'w', encoding = 'utf-8') as fout:
        for i in range(len(id_order)):
            # fout.write('%4d : %2d'%(id_order[i], labels[i]))
            fout.write(str(id_order[i]) + '\t' + str(labels[i]))
            fout.write('\n')
    # check(model, dict_name2id)
    