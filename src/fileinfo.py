import pandas as pd
plat_list = ['Teams', 'Zoom', 'Dingding', 'Tencent']
day1 = ['Tencent', 'Dingding', 'Teams', 'Zoom']
network_list = ['Wifi', '4G']

color_list = ['red', 'blue', 'green', 'orange']
video_list = ['English with OBS', 'Chinese with OBS',
              'English with Screen-Sharing', 'Chinese with Screen-Sharing']
Receiver_Network_Speed = ['93.57', '97.46', '65.8', '40.49']
Network_Speed = ['75.5', '92.87', '79.36', '33.99', '75.5', '92.87', '79.36',
                 '33.99', '75.5', '92.87', '79.36', '33.99', '110.69', '104.98', '85.89', '46.01']
Sender_Network_Speed = ['3.82', '5.27', '0.43', '17.99']

sender_PC = "MacBook Pro2020, Memory: 16G, CPU: Intel Core I5, modem: AirPort Extreme (0x14E7, 0x7BF)"
receiver_PC = "Thinkpad X1 Carbon 2018, Memory: 8G, CPU: Intel Core I7, modem: Intel(R) Ethernet Connection (4) I219-V"

sender_Phone = "iPhone 8 plus, modem: Intel XMM7480"
receiver_Phone = "iPhone XR, modem: Intel XMM7560"
results = []
for i in range(4):
    results.append({
        'fileNo': i + 1,
        'network': 'Wifi',
        'platform': day1[i],
        'netspeed': min(Sender_Network_Speed[0], Receiver_Network_Speed[1])
    })
for i in range(4):
    results.append({
        'fileNo': i + 5,
        'network': '4G',
        'platform': day1[i],
        'netspeed': min(Sender_Network_Speed[0], Receiver_Network_Speed[1])
    })
    filename = 'readme'+str(i+5)+'.txt'
for plat_type in range(4):
    for network_type in range(2):
        for video_type in range(4):
            i = plat_type * 8 + network_type * 4 + video_type + 9
            results.append({
                'fileNo': i,
                'network': network_list[network_type],
                'platform': plat_list[plat_type],
                'netspeed': Network_Speed[plat_type*4+network_type*2+1]
            })

pd.DataFrame(results).to_csv("../fileinfonew.csv", index=False)
