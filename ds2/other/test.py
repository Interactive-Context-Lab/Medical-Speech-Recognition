import torch
import numpy as np

network_output = torch.load("/home/ee303/Documents/test.pt")
seq = torch.load("/home/ee303/Documents/seq.pt")
# max_index = np.arange(to_numpy.shape[0]*to_numpy.shape[1])
# max_index = max_index.reshape(to_numpy.shape)
# max_index = max_index % to_numpy.shape[1]
# max_index = max_index[np.arange(len(to_numpy)), np.argmax(to_numpy, axis=1)]
# for i in max_index:
result_list = []
len_each_batch = []
batch_size, _, word_dim = network_output.shape
for index, batch in enumerate(network_output):
    to_numpy = batch.numpy()
    temp_array = []
    temp_int = -1
    for c,i in enumerate(np.concatenate((np.argmax(to_numpy,axis=1).reshape((-1,1)),np.max(to_numpy,axis=1).reshape(-1,1)),axis=1)):
        if c == seq[index]:
            break
        if i[0] == 0 and temp_int == 0 and i[1] > 0.95:
            pass
        else:
            temp_array.append(to_numpy[c])
        temp_int = i[0]
    result_list.append(temp_array)
    len_each_batch.append(len(temp_array))
result_array = np.zeros((batch_size, np.max(len_each_batch), word_dim))

temp_result = []
temp_len = []
for i in sorted(range(len(len_each_batch)), key=lambda k: len_each_batch[k], reverse=True):
    temp_result.append(result_list[i])
    temp_len.append(len_each_batch[i])
result_list = temp_result
len_each_batch = temp_len

for index, value in enumerate(len_each_batch):
    result_array[index][:value] = result_list[index]
len_each_batch = np.array(len_each_batch)
