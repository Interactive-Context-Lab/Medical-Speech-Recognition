import json

with open("/home/ee303/Documents/deepspeech.pytorch/500_manifest/mandarin_train.csv") as f:
    contents = f.readlines()
label_list = []
for line in contents:
    txt_file = line.strip().split(',')[1]
    with open(txt_file) as f:
        label = f.readlines()
    for a in label[0].strip():
        if not a in label_list:
            label_list.append(a)
            print(a)

with open("/home/ee303/Documents/deepspeech.pytorch/mandarin/madarin_class.json", 'w') as f:
    f.write('[')
    for i in label_list:
        f.write('"%s", '%(i))
    f.write(']')




