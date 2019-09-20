import os


with open("/home/ee303/Documents/data/data_aishell/transcript/aishell_transcript_v0.8.txt", 'r') as f:
    labels = f.readlines()

labels = [a.strip() for a in labels]
label_dict = {}

for line in labels:
    wavname = line.split(" ", 1)[0]
    label_content = line.split(" ", 1)[1].replace(' ', '')
    label_dict[wavname] = label_content

list_dirs = os.walk("/home/ee303/Documents/data/data_aishell/wav/train")
with open("/home/ee303/Documents/data/data_aishell/AISHELL_train.csv", "w") as mf:
    for root, dirs, files in list_dirs:
        for f in files:
            if os.path.splitext(f)[1] == '.wav' and os.path.splitext(f)[0] in label_dict:
                fn = os.path.splitext(f)[0]
                with open("/home/ee303/Documents/data/data_aishell/transcript/train/" + fn + '.txt', 'w') as lf:
                    lf.write(label_dict[fn])
                mf.write(os.path.join(root, f) + ',' + os.path.join("/home/ee303/Documents/data/data_aishell/transcript/train", fn + '.txt') + '\n')






