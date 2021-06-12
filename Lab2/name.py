import json
import matplotlib.pyplot as plt
import math
# 每个json文件为一组下所有视频的计算结果。
# json文件的结构如下：
# {
#   视频文件名: [[blur], [noise], [freeze]],
#   ...
# }


plat_list = ['teams', 'zoom', 'ding', 'tencent']
data_list = [0,0,0,0]
# 画图分类
network_list = ['_4g','_wifi','_5g']
video_list = ['_out','_in','_zh_obs','_en_obs','_zn_share','_en_share']
color_list = ['red','blue','green','orange']
# filename = '1.json'
videoname = []
for i in range(1,7):
    filename = str(i)+'.json'
    
    with open(filename, 'r') as f:
        # print(filename)
        data = json.load(f)
        videoname += data.keys()
        
for j in sorted(videoname):
    print(j)
