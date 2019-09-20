import os


for i in range(10):
    with open("/home/ee303/Documents/data/record/test_smalldif/" + str(i + 1) + ".txt", 'r') as f:
        labels = f.readlines()

    labels = [a.strip() for a in labels]
    label_dict = {}

    for line in labels:
        wavname = line.split("\t")[0]
        label_content = line.split("\t")[1]
        label_dict[wavname] = label_content

    # list_dirs = os.walk("/home/ee303/Documents/data/record/test")
    # with open("../500_manifest/test_difsent", "w") as mf:
    #     for root, dirs, files in list_dirs:
    #         for f in files:
    #             if os.path.splitext(f)[1] == '.wav' and os.path.splitext(f)[0] in label_dict:
    #                 fn = os.path.splitext(f)[0]
    #                 with open("/home/ee303/Documents/data/record/test/label/" + fn + '.txt', 'w') as lf:
    #                     lf.write(label_dict[fn])
    #                 mf.write(os.path.join(root, f) + ',' + os.path.join("/home/ee303/Documents/data/record/test/label", fn + '.txt') + '\n')

    for fname in label_dict.keys():
        with open('/home/ee303/Documents/data/record/test_smalldif/label/' + fname + '.txt', 'a') as f:
            f.write(label_dict[fname])




