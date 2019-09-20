import os

train_manifest = "/data2/punctuation_AandB/5fold/5/train_manifest.csv"
output_path = "/data2/punctuation_AandB/5fold/5"

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


with open(train_manifest, "r") as f:
    train_files = f.readlines()
train_files = [a.strip().split(",")[-1] for a in train_files]

label_kinds = []
for i in train_files:
    with open(i, "r") as f:
        label = f.readlines()[0].strip()
    for j in sep_seq(label):
        if j not in label_kinds:
            label_kinds.append(j)

label_kinds.sort()
with open(os.path.join(output_path, "label.json"), "w") as f:
    f.write('["_", ')
    for j in label_kinds:
        f.write('"{}", '.format(j))
    f.write('"{<unk>}", " "]')



