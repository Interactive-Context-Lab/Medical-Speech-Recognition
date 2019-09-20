from jiwer import wer


with open("/home/ee303/Documents/ds2_pytorch_ME/result/Google_API/google_modified.txt", "r") as f:
    contents = f.readlines()

contents = [a.strip().replace(" ","").replace("{","").replace("}","") for a in contents]

total_num = 0
total_err = 0
Google_result = {}
for i in range(0, len(contents)-1, 3):
    Google_result[contents[i]] = {}
    Google_result[contents[i]]["ref"] = contents[i + 1]
    Google_result[contents[i]]["hyp"] = contents[i + 2]

    ref = contents[i + 1]
    hyp = contents[i + 2]
    if ref == "":
        ref = " "
    total_num += len(list(ref))
    if hyp == "":
        hyp = " "
    error_rate = wer(list(ref), list(hyp))
    total_err += int(error_rate * len(list(ref)))
    Google_result[contents[i]]["cer"] = error_rate

with open("/home/ee303/Documents/ds2_pytorch_ME/result/Google_API/Google_CER.txt", "w") as f:
    for i in Google_result.keys():
        f.write(i + "\n")
        f.write("ref:" + Google_result[i]["ref"] + "\n")
        f.write("hyp:" + Google_result[i]["hyp"] + "\n")
        f.write(str(Google_result[i]["cer"]) + "\n")
    f.write(str(total_err/total_num))