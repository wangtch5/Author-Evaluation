from db_utils import * 
import numpy as np
# 根据google的计算机大类下期刊分类情况，统计不同领域的fos频率近似为概率

def venue_fos(coll, venue):
    dict_fos = {}
    for each in coll.find({"venue":venue}):
        try:
            for name in each["fos"]:
                if name in dict_fos:
                    dict_fos[name] += 1
                else:
                    dict_fos[name] = 1
        except Exception:
            print("no such key: fos")
    
    return dict_fos

def dict_update(dic1, dic2):
    for each in dic2:
        if each in dic1:
            dic2[each] += dic1[each]
    dic1.update(dic2)
    
    return dic1

def recursion(lis, i):
    if i > 0:
        lis[i-1]  = dict_update(lis[i-1], lis[i])
        recursion(lis, i-1)
    
    return lis[0]
    
def venue_fos_summary(coll, venue_lis, freq = True):
    venue_fos_lis = []
    for each in venue_lis:
        venue_fos_lis.append(venue_fos(coll, each))

    dic = recursion(venue_fos_lis, len(venue_fos_lis)-1)
    
    if freq:
        total = sum(dic.values())
        for each in dic:
            dic[each] /= total
    
    return dic

def write_local(path, dic):
    with open('./venue_fos/'+path, 'w', encoding = 'utf-8') as f:
        for each in dic:
            # print(each)
            f.write(str(each[0]) + '\t' + str(each[1]))
            f.write('\n')
    print(path, 'write to local')
    
if __name__ == "__main__":
	aminer = DataBase("mongodb://root:sysu2016@222.200.166.138:8815", "research_data", "com_en")
	coll = aminer.collection
	
	Robotics = ["The International Journal of Robotics Research",\
	"Robotics and Autonomous Systems","Autonomous Robots","Mechatronics"]
	
	HCI = ["Behaviour & Information Technology", "IEEE Transactions on Affective Computing"]
	
	SoftwareSys = ["IEEE Transactions on Software Engineering", "Journal of Systems and Software",\
	"IEEE Software", "Empirical Software Engineering"]
	
	HardwareDesign = ["IEEE Transactions on Computers"]
	
	ComputerVision = ["IEEE Transactions on Pattern Analysis and Machine Intelligence",\
	"IEEE Transactions on Image Processing", "Pattern Recognition", "International Journal of Computer Vision",\
	"Medical Image Analysis"]
	
	AI = ["Knowledge Based Systems", "Neural Networks", "Engineering Applications of Artificial Intelligence",\
	"Neural Computing and Applications"]
	
	TheoreticalCS = ["Journal of Computer and System Sciences", "SIAM Journal on Computing", \
	"Theoretical Computer Science"]
	
	Crypotography = ["IEEE Transactions on Information Forensics and Security", "Computers & Security",\
	"IEEE Transactions on Dependable and Secure Computing"]
	
	DataBaseSys = ["IEEE Transactions on Knowledge and Data Engineering", "Knowledge and Information Systems"]
	
	item = Robotics
	dic = venue_fos_summary(coll, item)
	dic = sorted(dic.items(), key = lambda x: x[1], reverse = True)
	write_local('Robotics.txt', dic)
    

    