import json
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
# 每个json文件为一组下所有视频的计算结果。
# json文件的结构如下：
# {
#   视频文件名: [[blur], [noise], [freeze]],
#   ...
# }


plat_list = ['teams', 'zoom', 'ding', 'tencent']
data_list = {'blur':{'teams':[],'zoom':[],'ding':[],'tencent':[]},'noise':{'teams':[],'zoom':[],'ding':[],'tencent':[]},'freeze':{'teams':[],'zoom':[],'ding':[],'tencent':[]}}
# 画图分类
network_list = ['_4g','_wifi','_5g']
video_list = ['_out','_in','_zh_obs','_en_obs','_zn_share','_en_share']
color_list = ['red','blue','green','orange']
type_list = ['.mp4','.mkv']
Metrics_list = ['Blur', 'Noise', 'Freeze']
metrics_list = ['blur', 'noise', 'freeze']
missing_list = ['' for i in range(12)]



for filenumber in range(1,7):
    filename = str(filenumber)+'.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        for i in data.keys():
            for k in range(3):
                # tmp_avg = sum(data[i][k])/len(data[i][k])
                tmp_avg = np.std(np.array(data[i][k]),ddof=1)
                # print(len(data[i][0]))
                for j in range(4):
                    if plat_list[j] in i:
                        if tmp_avg <= 20000:
                            data_list[metrics_list[k]][plat_list[j]].append(tmp_avg)
                        else: 
                            missing_list[k*4+j] = '*'

# print(data_list)
    
for k in range(3):
    plt.figure(figsize=(18, 8))
    # plt.xlim((0, 300))    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel(Metrics_list[k],fontsize=16) 
    plt.ylabel('Density',fontsize=16) 

    for i in range(4):
        pd.Series(data_list[metrics_list[k]][plat_list[i]]).plot(kind = 'kde')
    plt.legend(('teams'+missing_list[k*4],'zoom'+missing_list[k*4+1],'ding'+missing_list[k*4+2],'tencent'+missing_list[k*4+3]),loc = 'best',fontsize=16)

    plt.grid()
    
    plt.title('Density of Standard Deviation '+Metrics_list[k]+' on Different Apps',fontsize=20)
    plt.savefig(metrics_list[k]+'std.pdf',bbox_inches = 'tight')
