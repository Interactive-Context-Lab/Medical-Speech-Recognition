import json
from decoder import GreedyDecoder

with open("/home/ee303/Documents/data/real_record_labeled/annotated_audio/label.json") as label_file:
    labels = str(','.join(json.load(label_file)))
labels = labels.split(",")
labels_map = dict([(labels[i], i) for i in range(len(labels))])



transcript = "那他那時候開刀六月二十八號開刀的時候有備血兩u是沒有用的"
temp = []
is_eng_word = False
word_temp = ""
for c in transcript:
    word_temp = word_temp + c
    if c == "{" or c == "}":
        is_eng_word = not is_eng_word
        if not is_eng_word:
            if word_temp in labels_map:
                temp.append(labels_map.get(word_temp))
            else:
                temp.append(labels_map.get("<unk>"))
            word_temp = ""
    elif not is_eng_word:
        if word_temp in labels_map:
            temp.append(labels_map.get(word_temp))
        else:
            temp.append(labels_map.get("<unk>"))
        word_temp = ""
print(temp)

print([labels[a] for a in temp])

# with open("/home/ee303/Documents/data/real_record_labeled/annotated_audio/label.json") as label_file:
#     labels = str(','.join(json.load(label_file)))
#
# decoder = GreedyDecoder(labels)
# target_strings = decoder.convert_to_strings([[1073, 472, 1612, 24, 336, 912, 1011, 931, 1612]])

