from db_utils import DataBase
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def draw_bar(dic, path, y_label):
    print(dic)
    plt.figure(figsize=(12,12))
    xrow = tuple(dic.keys())
    x = np.arange(len(xrow))
    yrow = list(dic.values())
    print(x,yrow,xrow)
    plt.bar(x, yrow)
    plt.xticks(x, xrow, rotation=50, fontsize=12)
    plt.ylabel(y_label, fontsize=15)
    plt.savefig(path+".png")

def draw_line(dic, path, flag=0):
    # print(dic)
    print("draw_line...")
    plt.figure(figsize=(10,10))

    author =[]
    for name in dic:
        count = []
        citation = []
        xlabel = []
        author.append(name)
        for each in dic[name]:
            xlabel.append(each)
            try:
                count.append(dic[name][each]["count"])
                citation.append(dic[name][each]["citation"])
            except Exception:
                count.append(0)
                citation.append(0)
        x = np.arange(len(xlabel))
        if flag == 0:
            plt.plot(x[1:], count[1:], '--', linewidth=3, alpha=0.8, label=name)
        else:
            plt.plot(x[1:], citation[1:], '--', linewidth=3, alpha=0.8, label=name)
        
    xlabel[0] = "before2010"
    plt.legend()
    if flag == 0:
        plt.ylabel("paper number", fontsize=15)
    else:
        plt.ylabel("citation number", fontsize=15)
    plt.title(path[10:])
    plt.xlabel("year", fontsize=15)
    plt.xticks(x[1:], xlabel[1:])
    plt.savefig(path+'.png')

def total_citation(coll, name):
    data = coll.find({"authors":{"$elemMatch":{"name":name}}})
    citation = 0
    for each in data:
        try:
            citation += each["n_citation"]
        except Exception:
            continue
    return citation

def total_paper(coll, name):
    tem = year_paper_count(coll, name, 1, flag = 1)
    
    return {name:tem["count"]}
    
# flag = 1, gt; flag = -1, lt; flag = 0, equal.
def year_paper_count(coll, name, year, flag = 0):  
    if flag == 1:
        tem = coll.aggregate([{"$match":{"year":{"$gt":year}, "authors":{"$elemMatch":{"name":name}}}},
            {"$group":{"_id":name, "count":{"$sum":1}, "citation":{"$sum":"$n_citation"}}}
        ])
    elif flag == -1:
        tem = coll.aggregate([{"$match":{"year":{"$lt":year}, "authors":{"$elemMatch":{"name":name}}}},
            {"$group":{"_id":name, "count":{"$sum":1}, "citation":{"$sum":"$n_citation"}}}
        ])
    else:
        tem = coll.aggregate([{"$match":{"year":year, "authors":{"$elemMatch":{"name":name}}}},
            {"$group":{"_id":name, "count":{"$sum":1}, "citation":{"$sum":"$n_citation"}}}
        ])
    dic = {}
    for each in tem:
        dic = {"count":each["count"], "citation":each["citation"]}  
    
    return dic  

def summary(coll, names):
    dic_summ = {}
    for name in names:
        dic_summ[name] = {}
        dic_summ[name]["bf2010"] = year_paper_count(coll, name, 2010, flag = -1)
        for year in [2010, 2011, 2012, 2013, 2014]:
            dic_summ[name][str(year)] = year_paper_count(coll, name, year)
    
    return dic_summ

def summary_all(coll, names): 
    dic_paper = {}
    dic_cit = {}
    for name in names:
        dic_paper.update(total_paper(coll, name))
        dic_cit[name] = total_citation(coll, name)
    
    return dic_paper, dic_cit

if __name__ == "__main__":
    aminer = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
    coll = aminer.collection
    method1 = ["Wei Wang", "Philip S. Yu", "Jiawei Han", "Jun Zhang", "Ian F. Akyildiz", "Sebastian Thrun", "Yu Wang", "Zhi-Hua Zhou", "Wei Chen", "Gilbert Laporte"]
    method2 = ["Wei Wang", "Philip S. Yu", "Jiawei Han", "Jun Zhang", "Ian F. Akyildiz", "Sebastian Thrun", "Zhi-Hua Zhou", "Wei Chen", "Hui Li", "Lei Chen"]
    hindex = ["Jiawei Han", "Wei Wang", "Philip S. Yu", "Hector Garcia-Molina", "Sebastian Thrun", "Deborah Estrin", "Daphne Koller", "Christos Faloutsos", "Gilbert Laporte", "John A. Stankovic"]
    allname = set(method1 + method2 + hindex)
    
    # hindex_result = summary(coll, hindex)
    # draw_line(hindex_result, './picture/lineplot_hindex_paper')
    # draw_line(hindex_result, './picture/lineplot_hindex_cit',1)
    # method1_result = summary(coll, method1)
    # draw_line(method1_result, './picture/lineplot_method1_paper')
    # draw_line(method1_result, './picture/lineplot_method1_cit',1)
    method2_result = summary(coll, method2)
    draw_line(method2_result, './picture/lineplot_method2_paper')
    draw_line(method2_result, './picture/lineplot_method2_cit',1)
    
    
    # dic_paper, dic_cit = summary_all(coll, allname)
    # draw_bar(dic_cit, './picture/barplot_citation', 'citation number')
    # draw_bar(dic_paper, './picture/barplot_paper', 'paper number')
    
    
