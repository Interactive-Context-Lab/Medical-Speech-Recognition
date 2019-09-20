

for i in range(1,10):
    with open("/home/ee303/Documents/deepspeech.pytorch/results/test/" + str(i) + '.txt') as f:
        pred = f.readlines()

    pred_dict = {}

    for a in range(int((len(pred)-1)/3)):
        key = pred[a*3].split("\n")[0].split(':')[1]
        pred_dict[key] = ''.join(pred[a*3:a*3+3])

    with open("/home/ee303/Documents/deepspeech.pytorch/results/test/" + str(i) + '_align.txt', 'w') as f:
        for a in range(40):
            with open("/home/ee303/Documents/data/nurse_test/label/" + str(i) + "_" + str(a+1) + ".txt", 'r') as l:
                key = l.readlines()[0].strip().split('\t')[1]
                f.write(pred_dict[key])

        f.write(pred[-1])