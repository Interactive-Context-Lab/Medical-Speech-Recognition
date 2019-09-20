import os
import json


with open("/home/ee303/Documents/data/primewords_md_2018_set1/set1_transcript.json", 'r') as f:
    labels = json.load(f)

label_dict = {}

for line in labels:
    wavname = line['file']
    label_content = line['text'].replace(' ', '')
    label_dict[wavname] = label_content

list_dirs = os.walk("/home/ee303/Documents/data/primewords_md_2018_set1/audio_files")
with open("/home/ee303/Documents/data/primewords_md_2018_set1/primewords.csv", "w") as mf:
    for root, dirs, files in list_dirs:
        for f in files:
            if os.path.splitext(f)[1] == '.wav' and f in label_dict:
                fn = os.path.splitext(f)[0]
                with open("/home/ee303/Documents/data/primewords_md_2018_set1/label/" + os.path.splitext(f)[0] + '.txt', 'w') as lf:
                    lf.write(label_dict[f])
                mf.write(os.path.join(root, f) + ',' + os.path.join("/home/ee303/Documents/data/primewords_md_2018_set1/label", fn + '.txt') + '\n')






