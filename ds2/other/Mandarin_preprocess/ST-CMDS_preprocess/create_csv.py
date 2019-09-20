import os

file_list = os.listdir("/home/ee303/Documents/data/ST-CMDS-20170001_1-OS")

wav_files = []
txt_files = []

for file in file_list:
    if os.path.splitext(file)[1] == '.wav':
        wav_files.append(os.path.splitext(file)[0])
    elif os.path.splitext(file)[1] == '.txt':
        txt_files.append(os.path.splitext(file)[0])

with open('/home/ee303/Documents/data/ST-CMDS.csv','w') as f:
    for each_wav in wav_files:
        if each_wav in txt_files:
            f.write(os.path.join("/home/ee303/Documents/data/ST-CMDS-20170001_1-OS", each_wav + ".wav") + ',' + os.path.join("/home/ee303/Documents/data/ST-CMDS-20170001_1-OS", each_wav + ".txt") + '\n')
        print(each_wav)
