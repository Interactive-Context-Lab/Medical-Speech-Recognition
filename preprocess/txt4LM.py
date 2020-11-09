"""
Step 3 of pre-processing

Given the syllable manifest and E2C.json obtained at step 2,
this program will generate training manifest, test manifest, language model, and label categories of 5-fold.
Every fold will augment training data 3 times using wave augmentation.

:data_manifest: the syllable manifest obtained at step 2
:E2C_file: obtained at step 2
:splice_manifest: the path about the splice augmentation data
:lm_cmd_path: the path of language model's executable file
:out_file: path to save each fold
"""

import numpy as np
import os
import random
import librosa
import json

data_manifest = "/2TB/MEDICIC/BC/A_Pretrain/baseline/train_manifest.csv"
E2C_file = "/2TB/MEDICIC/BC/A_Pretrain/baseline/E2C.json"
lm_cmd_path = "/home/ee303/Downloads/kenlm/build/bin/lmplz"
out_file = "/2TB/MEDICIC/BC/A_Pretrain/baseline"

def sep_seq(seq):
    """
    return a list of sentence
    e.g. "Ada{asd}qe{qs}a" -> [A,s,a,{asd},q,e,{qs},a]

    :param seq: input sentence
    :return: list of sentence
    """
    temp = []
    is_eng_word = False
    word_temp = ""
    for c in seq:
        word_temp = word_temp + c
        if c == "{" or c == "}" or c == "<" or c == ">":
            is_eng_word = not is_eng_word
            if not is_eng_word:
                temp.append(word_temp)
                word_temp = ""
        elif not is_eng_word:
            temp.append(word_temp)
            word_temp = ""
    return temp

# load all data's path
with open(data_manifest, "r") as f:
    data = f.readlines()
data = [a.strip() for a in data]

# load E2C_file and replace English words by corresponding chinese words in text label
# the replaced text is used to train language model
with open(E2C_file) as label_file:
    E2C = json.load(label_file)
with open(os.path.join(out_file, "txt4LM.txt"), "w") as f:
    for j in data:
        with open(j.strip().split(",")[1], "r") as lf:
            label = lf.readlines()[0].strip()
            print(label)
        for k in E2C.keys():
            if k in label:
                label = label.replace(k, E2C[k])
        f.write(" ".join(label) + "\n")
# # command = lm_cmd_path + " -o 2 --discount_fallback <" + os.path.join(out_file, "txt4LM.txt") +" >" + os.path.join(out_file,"2.arpa")
command = lm_cmd_path + " -o 5 --discount_fallback <" + os.path.join(out_file, "txt4LM.txt") +" > " + os.path.join(out_file,"5.arpa")
os.system(command)
