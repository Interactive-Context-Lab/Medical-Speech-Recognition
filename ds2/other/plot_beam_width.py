import numpy as np
import matplotlib.pyplot as plt


width_range = list(range(10,100,10)) + list(range(100,300,50))
# width_range = list(range(10,100,10))

width_CER_list = []
width_time_list = []


for a in width_range:
    with open("/data2/train_result/result/normal_splice_spec/modify_beam_width/" + str(a) + ".txt", 'r') as f:
        content = f.readlines()
    CER = content[-2].strip().split(' ')[-1]
    time = content[-1].strip().split(':')[-1]
    width_CER_list.append(float(CER))
    width_time_list.append(float(time))


Greedy_CER_list = np.array(width_CER_list)


fig = plt.figure()

ax1 = fig.add_subplot(111)
lns1 = ax1.plot(width_range, width_CER_list, linestyle='-', marker = "o",label = "CER")
ax1.set_ylabel('CER')
# ax1.set_title("Double Y axis")
ax1.set_xlabel('Beam Width')

ax2 = ax1.twinx()  # this is the important function
lns2 = ax2.plot(width_range, width_time_list, linestyle='--', marker = "^", color = "red", label = "Time")
ax2.set_ylabel('Seconds')
ax2.set_xlabel('Beam Width')

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=9)

plt.show()

# x = np.arange(0., np.e, 0.01)
# y1 = np.exp(-x)
# y2 = np.log(x)
#
# fig = plt.figure()
#
# ax1 = fig.add_subplot(111)
# ax1.plot(x, y1)
# ax1.set_ylabel('Y values for exp(-x)')
# ax1.set_title("Double Y axis")
#
# ax2 = ax1.twinx()  # this is the important function
# ax2.plot(x, y2, 'r')
# ax2.set_xlim([0, np.e])
# ax2.set_ylabel('Y values for ln(x)')
# ax2.set_xlabel('Same X for both exp(-x) and ln(x)')

plt.show()

# plt.plot(width_range, Greedy_CER_list)
# plt.xlabel('Beam width')
# plt.ylabel('CER')
# plt.show()


