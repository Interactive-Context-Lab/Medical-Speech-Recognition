from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
# X = np.arange(0.2, 3.1, 0.2)
X = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2]
# Y = np.arange(0, 15, 2)
Y = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]
Z = np.zeros(shape=(len(Y),len(X)))

for x in range(len(X)):
    for y in range(len(Y)):
        with open("/data2/train_result/result/normal_splice_spec/LM_hyperparameter/" + str(round(X[x], 1)) + '_' + str(Y[y]) + ".txt", 'r') as f:
            content = f.readlines()
        CER = content[-2].strip().split(' ')[-1]
        # CER = content[-1].split(' sec')[0].split(': ')[-1]
        print(str(round(X[x], 1)) + '\t' + str(Y[y]) + "\t" + CER)
        Z[y][x] = CER
X, Y = np.meshgrid(X, Y)

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
ax.set_zlabel('CER')
ax.set_ylabel('Beta')
ax.set_xlabel('Alpha')
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
