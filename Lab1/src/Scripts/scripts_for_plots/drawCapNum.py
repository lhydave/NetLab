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
	for video_type in range(4):
		offset = network_type * 4 + video_type


		plt.figure(figsize=(20, 8))
		plt.xlim((0, 300))
		plt.xlabel("Time (s)") 
		plt.ylabel("Average Packet Number") 
		plt.grid()
		plt.title(network_list[network_type] + ", " + video_list[video_type])

		for plat_type in range (4):

			pcap_path = "test"+str(plat_type*8+offset+9)+".pcapng"
			packets = sp.rdpcap(pcap_path)

			print("load done")
			start_time = packets[0].time
			total_time = math.ceil(packets[-1].time - start_time)



			cnt_total_length = [0 for i in range(total_time)]
			cnt_total_number = [0 for i in range(total_time)]
			cnt_aver_length = [0 for i in range(total_time)]
			src_cnt = dict()
			dst_cnt = dict()

			for i in range(100):
			    if packets[i].haslayer("UDP") and packets[i].haslayer("IP"):
			        ip = packets[i].getlayer("IP")
			        temp_src = ip.src
			        temp_dst = ip.dst
			        if temp_src in src_cnt:
			            src_cnt[temp_src] += 1
			        else:
			            src_cnt[temp_src] = 1
			        if temp_dst in dst_cnt:
			            dst_cnt[temp_dst] += 1
			        else:
			            dst_cnt[temp_dst] = 1


			src_target = max(src_cnt, key=src_cnt.get)
			dst_target = max(dst_cnt, key=dst_cnt.get)
			print(src_target, dst_target)


			def g(x):
			    if x.haslayer("UDP") and x.haslayer("IP"):
			        ip_x = x.getlayer("IP")
			        return (ip_x.src == src_target and ip_x.dst == dst_target)
			    return False


			packets = list(filter(g, packets))
			for i in packets:
				cnt_total_length[int(i.time - start_time)] += len(sp.corrupt_bytes(i))
				cnt_total_number[int(i.time - start_time)] += 1
			for i in range(total_time):
				if cnt_total_number[i] != 0:
					cnt_aver_length[i] = cnt_total_length[i] / cnt_total_number[i]
			cnt_total_length.pop()
			cnt_total_number.pop()
			cnt_aver_length.pop()

			plt.plot(range(len(cnt_total_number)), cnt_total_number,color=color_list[plat_type],label = plat_list[plat_type])

		plt.legend()

		plt.savefig(network_list[network_type] + " " + video_list[video_type]+'Packet Number.pdf')
		# plt.show()