import json
import os

train_manifest = "/data2/punctuation_AandB/5fold/5/train_manifest.csv"
E2C_file = "/data2/punctuation_AandB/5fold/E2C.json"
lm_cmd_path = "/home/ee303/Downloads/kenlm/build/bin/lmplz"
store_path = "//data2/punctuation_AandB/5fold/5"

origin_data_words = ["/home/ee303/Documents/data/real_record_labeled/annotated_audio/audio","/data2/punctuation_B/preprocessed/wave"]

with open(train_manifest, "r") as f:
    train_files = f.readlines()
train_files = [a.strip().split(",")[-1] for a in train_files for b in origin_data_words if b in a]

with open(E2C_file) as label_file:
    E2C = json.load(label_file)

with open(os.path.join(store_path,"txt4LM.txt"), "w") as f:
    for i in train_files:
        with open(i, "r") as lf:
            label = lf.readlines()[0].strip()
        for j in E2C.keys():
            if j in label:
                label = label.replace(j, E2C[j])
        f.write(" ".join(label) + "\n")

command = lm_cmd_path + " -o 5 <" + os.path.join(store_path, "txt4LM.txt") +" >" + os.path.join(store_path,"5.arpa")
os.system(command)

