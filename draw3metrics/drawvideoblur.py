from scapy import all as sp
import matplotlib.pyplot as plt
import math
import csv

plat_list = ['Teams', 'Zoom', 'Dingding', 'Tencent']
day1= ['Tencent', 'Dingding', 'Teams', 'Zoom']
network_list = ['Wifi to Wifi', '4G to 4G']

color_list = ['red','blue','green','orange']
video_list = ['English with OBS', 'Chinese with OBS', 'English with Screen-Sharing', 'Chinese with Screen-Sharing']
Receiver_Network_Speed = ['70.4','51.76','93.57','97.46','65.8','40.49','79.36','33.99','110.69','104.98','85.89','46.01']
Sender_Network_Speed = ['3.82','5.27','0.43','17.99']



for network_type in range(2):


		plt.figure(figsize=(20, 8))
		plt.xlim((0, 300))
		plt.xlabel("Time (s)") 
		plt.ylabel("Blur") 
		plt.grid()
		plt.title(network_list[network_type] + ", Real Person, Result on Blur")
		for plat_type in range (4):

			with open( "test"+str(network_type*4+plat_type+1)+"_video.csv", 'r') as csvfile:
				reader = csv.reader(csvfile)
				res = [row[1] for row in reader]

				res.pop(0)
				res = [float(i) for i in res]
				# print(res)
			x = range(len(res))
			x = [i*4 for i in x]
			print(x)
			plt.plot(x, res,color=color_list[plat_type],label = day1[plat_type])
			

		plt.legend()

		plt.savefig(network_list[network_type] + " real person video" + '.pdf',bbox_inches = 'tight')
		# plt.show()