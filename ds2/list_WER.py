import os


result_dir = "/data2/punctuation_AandB/5fold/1/results/beam"
epochs = 100

WER_list = []


for i in range(121,151):
    with open(os.path.join(result_dir, "{}.txt".format(str(i))),"r") as f:
        contents = f.readlines()
    contents = contents[-2].strip().split(" ")[-1]
    WER_list.append(contents)

with open(os.path.join(result_dir, "ALL_list.txt"), "w") as f:
    for num, WER in enumerate(WER_list):
        f.write(WER + "\n")

