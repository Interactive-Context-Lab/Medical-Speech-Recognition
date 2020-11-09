"""
Step 2 of pre-processing
Change the label of English words to syllable.

Given the manifest obtained by step 1, and the file including all English words with the corresponding syllables,
the program will store the label which the English words are changed to the corresponding syllables.
Also, the path of all audio and syllable file is stored in "syllable_manifest.csv" at syllable_label_dir.
The output file "E2C.json", and "C2E.json" are used for training the language model and test stage.

:data_manifest: list of all audio's and label's path, obtain from step 1
:word2syllable: contain english words anc corresponding syllables.
:syllable_label_dir: directory that stores syllable label.
:out_dir: directory that stores "syllable_manifest.csv", "E2C.json", and "C2E.json".
"""

import os
import json


data_manifest = "/media/ee303/fb8e9f58-5cbb-4101-97f4-60f30abdc05d/Chinese_Taiwanese_short/train_test_c_t_checked/manifest.csv"
word2syllable = "./word2syllable.txt"
syllable_label_dir = "/media/ee303/fb8e9f58-5cbb-4101-97f4-60f30abdc05d/Chinese_Taiwanese_short/train_test_c_t_checked/syllable_label"
out_dir = "/media/ee303/fb8e9f58-5cbb-4101-97f4-60f30abdc05d/Chinese_Taiwanese_short/train_test_c_t_checked"

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

# load the correspondence between words and syllables
with open(word2syllable, "r") as f:
    contents = f.readlines()
contents = [a.strip().split("\t") for a in contents]
contents = contents[:-26]
word2syllable_dict = {}
for i in contents:
    temp = ""
    for j in i[1].split(","):
        temp += "{" + j + "}"
    word2syllable_dict[i[0]] = temp

# a file to save the path of each sentence after converting English word to syllable
out_manifest = os.path.join(out_dir, "syllable_manifest.csv")

# convert English word to syllable and save the result in "syllable_label_dir"
other_words = []
eng_syllable = []
for i in data:
    audio_path = i.split(",")[0]
    label_path = i.split(",")[1]
    label_name = label_path.split("/")[-1]
    out_path = os.path.join(syllable_label_dir, label_name)
    with open(label_path, "r") as f:
        label = f.readlines()[0].strip()
    for key in word2syllable_dict.keys():
        if key in label:
            label = label.replace(key,word2syllable_dict[key])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(label)
    with open(out_manifest, "a") as f:
        f.write("{},{}\n".format(audio_path,out_path))
    label_list = sep_seq(label)
    for w in label_list:
        if len(w) > 1:
            if w not in eng_syllable:
                eng_syllable.append(w)
        else:
            if w not in other_words:
                other_words.append(w)

# English to word and word to English file
E2C_dic = {}
count = 19968
for i in eng_syllable:
    while i not in E2C_dic:
        if chr(count) in other_words:
            count = count + 1
        else:
            E2C_dic[i] = chr(count)
            count = count + 1
while 1:
    if chr(count) in other_words:
        count = count + 1
    else:
        E2C_dic['{<unk>}'] = chr(count)
        break

with open(os.path.join(out_dir,'E2C.json'), 'w') as outfile:
    json.dump(E2C_dic, outfile,ensure_ascii=False)
    outfile.write('\n')
C2E_dic = {}
for i in E2C_dic.keys():
    C2E_dic[E2C_dic[i]] = i
with open(os.path.join(out_dir,'C2E.json'), 'w') as outfile:
    json.dump(C2E_dic, outfile,ensure_ascii=False)
    outfile.write('\n')
