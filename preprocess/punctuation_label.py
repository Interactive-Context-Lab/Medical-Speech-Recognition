import os

target_file = "/home/ee303/Documents/data/real_record_labeled/annotated_audio/punctuation_label"
label_file = "/data2/A_punctuation.txt"
word2syllable = "/data2/data_B/word2syllable.txt"


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


with open(label_file, "r") as f:
    contents = f.readlines()

contents = [a.strip().split("\t") for a in contents]
contents[0][0] = contents[0][0][1:]


for i in contents:
    label_fname = os.path.join(target_file, i[0])
    label_context = i[1]
    label_context = label_context.replace(" ","").replace("、","，").replace("，","，").replace("。","，").replace(",","，").replace(".","").replace("/","").lower()
    for key in word2syllable_dict.keys():
        if key in label_context:
            label_context = label_context.replace(key,word2syllable_dict[key])
    with open(label_fname, "w") as f:
        f.write(label_context)

