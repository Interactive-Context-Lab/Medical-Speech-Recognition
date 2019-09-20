import numpy as np
import matplotlib.pyplot as plt


Greedy_CER_list = []

for a in range(1,51):
    with open("/home/ee303/Documents/deepspeech.pytorch/results/ATCOSIM/Greedy/" + str(a) + ".txt", 'r') as f:
        content = f.readlines()
    CER = content[-1].strip().split(' ')[-3].split('\t')[0]
    Greedy_CER_list.append(float(CER))

Greedy_CER_list = np.array(Greedy_CER_list)

Beam_CER_list = []

for a in range(1,51):
    with open("/home/ee303/Documents/deepspeech.pytorch/results/ATCOSIM/Beam/" + str(a) + ".txt", 'r') as f:
        content = f.readlines()
    CER = content[-1].strip().split(' ')[-3].split('\t')[0]
    Beam_CER_list.append(float(CER))

Beam_CER_list = np.array(Beam_CER_list)

Beam_lm_CER_list = []
for a in range(1,51):
    with open("/home/ee303/Documents/deepspeech.pytorch/results/ATCOSIM/Beam_lm/" + str(a) + ".txt", 'r') as f:
        content = f.readlines()
    CER = content[-1].strip().split(' ')[-3].split('\t')[0]
    Beam_lm_CER_list.append(float(CER))

Beam_lm_CER_list = np.array(Beam_lm_CER_list)


plt.xlabel('Epoch')
plt.ylabel('WER')

plt.plot(Greedy_CER_list, label = "Greedy")
plt.plot(Beam_CER_list, label = 'Beam Search')
plt.plot(Beam_lm_CER_list, label = 'Beam + LM')

plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.0)

plt.show()
