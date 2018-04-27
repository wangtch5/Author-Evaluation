import numpy as np


def prepare_testset(path='./cluster_id2label.txt'):
    dict_label2id = {}
    with open(path, 'r', encoding = 'utf-8') as f:
        for line in f:
            tem = line.strip().split('\t')
            if tem[1] in dict_label2id:
                dict_label2id[tem[1]].append(tem[0])
            else:
                dict_label2id[tem[1]] = []
    
    flag = 100
    dict_test = {}
    for each in dict_label2id:
        if len(dict_label2id[each]) >= flag:
            dict_test[each] = dict_label2id[each][:flag]
    test_id = []
    for each in dict_test:
        test_id.extend(dict_test[each])
        
    print(len(test_id))
    
    with open('./emb/authors.emb', 'r', encoding = 'utf-8') as g:
        with open('./emb/test_author.emb', 'w', encoding = 'utf-8') as h:
            i = 0 
            for line in g:
                if i == 0:
                    h.write(line)
                    i += 1
                    continue
                tem = line.strip().split(' ')
                if tem[0] in test_id:
                    h.write(line)

def precision(path1 = './test_kmeans_cluster_result.txt', path2 = './cluster_id2label.txt'):
    dict_kmeans_label = {}
    with open(path1, 'r', encoding = 'utf-8') as f1:
        for line in f1:
            tem = line.strip().split('\t')
            if tem[1] in dict_kmeans_label:
                dict_kmeans_label[tem[1]].append(tem[0])
            else:
                dict_kmeans_label[tem[1]] = []
    
    dict_test_label = {}
    with open(path2, 'r', encoding = 'utf-8') as f2:
        for line in f2:
            tem = line.strip().split('\t')
    #         if tem[1] in dict_test_label:
    #             dict_test_label[tem[1]].append(tem[0])
    #         else:
    #             dict_test_label[tem[1]] = []
            dict_test_label[tem[0]] = tem[1]
    print('data loaded...')
    
    summary = []
    for each in dict_kmeans_label:
        dict_summary = {}
        for i in dict_kmeans_label[each]:
            if dict_test_label[i] in dict_summary:
                dict_summary[dict_test_label[i]] += 1
            else:
                dict_summary[dict_test_label[i]] = 1
        summary.append(dict_summary)
    
    precision_ = []
    for each in summary:
        print(each)
        tem = np.array(list(each.values()))
        max_label_num = np.max(tem)
        total_label_num = np.sum(tem)
        precision_.append(max_label_num / total_label_num)
    
    print(precision_)

if __name__ == "__main__":
    # prepare_testset()
    precision()
    print('done!')
                