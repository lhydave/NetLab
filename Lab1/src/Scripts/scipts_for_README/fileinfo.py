plat_list = ['Teams', 'Zoom', 'Dingding', 'Tencent']
day1= ['Tencent', 'Dingding', 'Teams', 'Zoom']
network_list = ['Wifi to Wifi', '4G to 4G']

color_list = ['red','blue','green','orange']
video_list = ['English with OBS', 'Chinese with OBS', 'English with Screen-Sharing', 'Chinese with Screen-Sharing']
Receiver_Network_Speed = ['93.57','97.46','65.8','40.49']
Network_Speed = ['75.5','92.87','79.36','33.99','75.5','92.87','79.36','33.99','75.5','92.87','79.36','33.99','110.69','104.98','85.89','46.01']
Sender_Network_Speed = ['3.82','5.27','0.43','17.99']

sender_PC = "MacBook Pro2020, Memory: 16G, CPU: Intel Core I5, modem: AirPort Extreme (0x14E7, 0x7BF)"
receiver_PC = "Thinkpad X1 Carbon 2018, Memory: 8G, CPU: Intel Core I7, modem: Intel(R) Ethernet Connection (4) I219-V"

sender_Phone = "iPhone 8 plus, modem: Intel XMM7480"
receiver_Phone = "iPhone XR, modem: Intel XMM7560"

for i in range(4):
	filename = 'README'+str(i+1)+''
	with open(filename, 'w') as file_object:
		file_object.write("Real Person, Wifi to Wifi, "+ day1[i]+"\n")
		file_object.write("Sender: \n")
		file_object.write("Upload speed "+str(Sender_Network_Speed[0])+" Mbps, and download speed "+str(Sender_Network_Speed[1])+" Mbps\n")
		file_object.write("placed at Jiayuan Dining Center 3rd floor\n")
		file_object.write("using "+sender_PC+"\n")
		file_object.write("\n")
		file_object.write("Receiver: \n")
		file_object.write("Upload speed "+str(Receiver_Network_Speed[0])+" Mbps, and download speed "+str(Receiver_Network_Speed[1])+" Mbps\n")
		file_object.write("place at Xintaiyang Student Center 2nd underground\n")
		file_object.write("using " + receiver_PC+"\n")
for i in range(4):
	filename = 'README'+str(i+5)
	with open(filename, 'w') as file_object:
		file_object.write("Real Person, 4G to 4G, "+ day1[i]+"\n")
		file_object.write("Sender: \n")
		file_object.write("Upload speed "+str(Sender_Network_Speed[0])+" Mbps, and download speed "+str(Sender_Network_Speed[1])+" Mbps\n")
		file_object.write("placed at Jiayuan Dining Center 3rd floor\n")
		file_object.write("using "+sender_PC+" and "+ sender_Phone+"\n")
		file_object.write("\n")
		file_object.write("Receiver: \n")
		file_object.write("Upload speed "+str(Receiver_Network_Speed[0])+" Mbps, and download speed "+str(Receiver_Network_Speed[1])+" Mbps\n")
		file_object.write("place at Xintaiyang Student Center 2nd underground\n")
		file_object.write("using " + receiver_PC+" and " + receiver_Phone+"\n")
for plat_type in range(4):
	for network_type in range(2):
		for video_type in range(4):
			filename = 'README'+str(plat_type*8+network_type * 4 + video_type+9)
			with open(filename, 'w') as file_object:
				file_object.write(video_list[video_type]+", "+network_list[network_type]+", "+ plat_list[plat_type]+"\n")
				file_object.write("Sender: \n")
				file_object.write("placed at Jiayuan Dining Center 3rd floor\n")
				file_object.write("using "+sender_PC+" and "+ sender_Phone+"\n")
				file_object.write("\n")
				file_object.write("Receiver: \n")
				file_object.write("Upload speed "+Network_Speed[plat_type*4+network_type*2]+" Mbps, and download speed "+Network_Speed[plat_type*4+network_type*2+1]+" Mbps\n")
				file_object.write("place at Xintaiyang Student Center 2nd underground\n")
				file_object.write("using " + receiver_PC+" and " + receiver_Phone+"\n")
