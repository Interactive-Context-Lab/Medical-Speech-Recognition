import os
import json


manifest_file = "/data2/punctuation_AandB/5fold/manifest_punctuation_AandB"
store_path = "/data2/punctuation_AandB/5fold"

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


with open(manifest_file, "r") as f:
    data_files = f.readlines()
data_files = [a.strip() for a in data_files]

eng_syllable = []
other_words = []
for i in data_files:
    label = i.split(",")[1]
    with open(label, "r") as f:
        content = f.readlines()[0].strip()
    for j in sep_seq(content):
        if len(j) > 1:
            eng_syllable.append(j)
        else:
            other_words.append(j)

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

with open(os.path.join(store_path,'E2C.json'), 'w') as outfile:
    json.dump(E2C_dic, outfile,ensure_ascii=False)
    outfile.write('\n')
C2E_dic = {}
for i in E2C_dic.keys():
    C2E_dic[E2C_dic[i]] = i
with open(os.path.join(store_path,'C2E.json'), 'w') as outfile:
    json.dump(C2E_dic, outfile,ensure_ascii=False)
    outfile.write('\n')

