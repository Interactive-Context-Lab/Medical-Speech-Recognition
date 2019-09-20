import os
from shutil import copytree

# target_dir = '/home/ee303/Documents/data/data_aishell/wav/dev/'
#
# for i in range(2,41):
#     file_name = os.path.join("/home/ee303/Documents/data/data_aishell/wav","dev (%s)"%(i))
#     copieds = os.listdir(file_name)
#     for f in copieds:
#         copytree(os.path.join("/home/ee303/Documents/data/data_aishell/wav","dev (%s)"%(i),f),os.path.join(target_dir,f))


# target_dir = '/home/ee303/Documents/data/data_aishell/wav/test/'
#
# for i in range(2,21):
#     file_name = os.path.join("/home/ee303/Documents/data/data_aishell/wav","test (%s)"%(i))
#     copieds = os.listdir(file_name)
#     for f in copieds:
#         copytree(os.path.join("/home/ee303/Documents/data/data_aishell/wav","test (%s)"%(i),f),os.path.join(target_dir,f))


target_dir = '/home/ee303/Documents/data/data_aishell/wav/train/'

for i in range(2,341):
    file_name = os.path.join("/home/ee303/Documents/data/data_aishell/wav","train (%s)"%(i))
    copieds = os.listdir(file_name)
    for f in copieds:
        copytree(os.path.join("/home/ee303/Documents/data/data_aishell/wav","train (%s)"%(i),f),os.path.join(target_dir,f))
