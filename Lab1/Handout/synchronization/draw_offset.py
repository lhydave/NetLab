import matplotlib.pyplot as plt
import argparse

f1 = open('./ding-wire_0_resultoff.txt','r')
f1 = f1.readlines()
dingding = []
for log in f1:
    lg = log.split(' ')
    i = float(lg[1][:-1])
    dingding.append(i)
#print(dingding)

f2 = open('./tencent-wire_0_resultoff.txt','r')
f2 = f2.readlines()
tencent = []
for log in f2:
    lg = log.split(' ')
    i = float(lg[1][:-1])
    tencent.append(i)
#print(tencent)

f3 = open('./zoom-wire_0_resultoff.txt','r')
f3 = f3.readlines()
zoom = []
for log in f3:
    lg = log.split(' ')
    i = float(lg[1][:-1])
    zoom.append(i)
#print(zoom)

f4 = open('./teams-wire_0_resultoff.txt','r')
f4 = f4.readlines()
teams = []
for log in f4:
    lg = log.split(' ')
    i = float(lg[1][:-1])
    teams.append(i)
#print(teams)

min_len = min(len(dingding), len(tencent), len(zoom), len(teams))

dingding = dingding[:min_len]
tencent = tencent[:min_len]
zoom = zoom[:min_len]
teams = teams[:min_len]


ti = []
for i in range(min_len):
    ti.append(i*4/60)
#print(ti)

plt.plot(ti, tencent, '.-',color = 'blue', label='Tencent Meeting')
plt.plot(ti, dingding, '.-',color = 'red', label='DingTalk')
plt.plot(ti, zoom, '.-', color = 'orange',label='Zoom')
plt.plot(ti, teams, '.-', color = 'green',label='Teams')

#plt.xticks(ti)  # 设置横坐标刻度为给定的年份
plt.xlabel('time') # 设置横坐标轴标题
plt.ylabel('offset(seconds))')
plt.legend() # 显示图例，即每条线对应 label 中的内容
plt.savefig('./wire_save_offset.png')
plt.show() # 显示图形