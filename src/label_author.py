import numpy as np
import json
import os
import sys
import io
# in order to make print work well
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# 给作者打标签（根据fos，相当于手动打标签）

FILE_PATH = []

def getFilePath(filepath):
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            getFilePath(fi_d)
        else:
            FILE_PATH.append(fi_d)

def read_class_fos(path_lis):
    fos_class = []
    for each in path_lis:
        i = 0
        fos_word = {}
        with open(each, encoding = 'utf-8') as f:
            for line in f:
                tem = line.strip().split('\t')
                fos_word[tem[0]] = float(tem[1])
                i += 1
                if i == 99:
                    break
        fos_class.append(fos_word)
    
    print('read class fos.')
    return fos_class

def read_author_fos(path = './dict_fos_author.json'):
    with open(path, 'r', encoding = 'utf-8') as f:
        fos_author = json.load(f)
    
    print('read author fos.')
    return fos_author

def get_label_author(fos_author, fos_class):
    author_label = {}
    author_score = {}
    
    for author in fos_author:
        fos = fos_author[author]
        label = 0
        score_lis = []
        for each in fos_class:
            score = 0
            for fos_i in fos:
                if fos_i in each:
                    score += fos[fos_i] * each[fos_i]
                else:
                    continue
            score_lis.append((label, score))
            label += 1
        
        author_score[author] = score_lis
    print('calculate label score for each author')
    
    for author in author_score:
        author_score[author] = sorted(author_score[author], key = lambda x: x[1], reverse = True)
        author_label[author] = author_score[author][0][0]
    
    print('calculate the label.')
    return author_label, author_score
    
if __name__ == "__main__":
    getFilePath('./venue_fos')
    class_fos = read_class_fos(FILE_PATH)
    author_fos = read_author_fos()
    
    author_label, author_score = get_label_author(author_fos, class_fos)
    # print(author_label)
    with open('dict_name2id.json', 'r', encoding = 'utf-8') as f:
        dict_name2id = json.load(f)
    
    with open('cluster_name2label.txt', 'w', encoding = 'utf-8') as g1:
        for each in author_label:
            g1.write(each + '\t' + str(author_label[each]))
            g1.write('\n')
    
    with open('cluster_id2label.txt', 'w', encoding = 'utf-8') as g2:
        for each in author_label:
            try:
                g2.write(str(dict_name2id[each]) + '\t' + str(author_label[each]))
                g2.write('\n')
            except Exception:
                continue
    print("done!")