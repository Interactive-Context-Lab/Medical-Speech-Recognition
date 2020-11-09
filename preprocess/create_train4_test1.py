"""
Step 3 of pre-processing

Given the syllable manifest and E2C.json obtained at step 2,
this program will generate training manifest, test manifest, language model, and label categories.
It will augment training data 3 times using wave augmentation.

:data_manifest: the syllable manifest obtained at step 2
:E2C_file: obtained at step 2
:splice_manifest: the path about the splice augmentation data
:lm_cmd_path: the path of language model's executable file
:out_file: path to save each fold
"""

import numpy as np
import os
import random
import librosa
import json

data_manifest = "/dataA/train_manifest.csv"
E2C_file = "/dataA/E2C.json"
lm_cmd_path = "/home/ee303/Downloads/kenlm/build/bin/lmplz"
out_file = "/dataA/baseline"

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

def sox_proceed(input_path,output_file):
    """
    Change the temp, pitch, and gain of audio.

    :param input_path: path of the wave file to be adjust
    :param output_file: directory to save the adjusted wave file
    :return: path of the adjusted wave file
    """
    # random select parameter used in sox
    tempo = str(round(np.random.uniform(0.7, 1.2), 2))
    pitch = str(random.randint(-500,500))
    gain = str(random.randint(-20,10))
    file_name = input_path.split("/")[-1].split(".")[0] + "_" + "_".join([tempo, pitch, gain])
    output_path = os.path.join(output_file, file_name + ".wav")
    command = "sox " + input_path + " " + output_path + " tempo " + tempo + " pitch " + pitch + " gain " + gain
    os.system(command)
    return output_path

def roll_audio(fn, sr=16000):
    """
    Shift and add white noise of audio.

    :param fn: path of the wave file to be adjust
    :param sr: sample rate of wave file
    """
    # read wave
    roll_length = random.randint(0,sr/100) #noise range 0~sr/100
    wave_data = librosa.core.load(fn, sr)[0]
    # roll
    wave_data = np.roll(wave_data, roll_length)
    SNR = random.randint(10,15)
    wave_data += wgn(wave_data, SNR)
    # write wave after roll
    librosa.output.write_wav(fn, wave_data, sr)

def wgn(x, snr):
    """
    Add white noise.

    :param x: origin wave data
    :param snr: Signal-to-noise ratio to add white noise
    :return: adjusted wave data
    """
    snr = 10**(snr/10.0)
    xpower = np.sum(x**2)/len(x)
    npower = xpower / snr
    return np.random.randn(len(x)) * np.sqrt(npower)

# load all data's path
with open(data_manifest, "r") as f:
    data = f.readlines()
data = [a.strip() for a in data]

# random shuffle and separate into 4:1
random.shuffle(data)
each_num = int(np.ceil(len(data)/5))

# generate components
train_data = data[each_num:]
test_data = data[:each_num]
if not os.path.exists(out_file): os.makedirs(out_file)

# load E2C_file and replace English words by corresponding chinese words in text label
# the replaced text is used to train language model
with open(E2C_file) as label_file:
    E2C = json.load(label_file)
with open(os.path.join(out_file, "txt4LM.txt"), "w") as f:
    for j in data:
        with open(j.strip().split(",")[1], "r") as lf:
            label = lf.readlines()[0].strip()
        for k in E2C.keys():
            if k in label:
                label = label.replace(k, E2C[k])
        f.write(" ".join(label) + "\n")
# command = lm_cmd_path + " -o 2 --discount_fallback <" + os.path.join(out_file, "txt4LM.txt") +" >" + os.path.join(out_file,"2.arpa")
command = lm_cmd_path + " -o 5 --discount_fallback <" + os.path.join(out_file, "txt4LM.txt") +" >" + os.path.join(out_file,"5.arpa")
os.system(command)

# save testing data
with open(os.path.join(out_file, "test_manifest.csv"), "w") as f:
    for j in test_data:
        f.write(j + "\n")

# save training data
label_kinds = []
aug_wav_path = os.path.join(out_file, "augment")
with open(os.path.join(out_file, "train_manifest.csv"), "w") as f:
    for j in data:
        f.write(j + "\n")
        label_file = j.strip().split(",")[1]
        with open(label_file, "r") as lf:
            label = lf.readlines()[0].strip()
        for k in sep_seq(label):
            if k not in label_kinds:
                label_kinds.append(k)
    if not os.path.isdir(aug_wav_path): os.mkdir(aug_wav_path)

    # every training data be augmented 3 times by wave augmentation
    for _ in range(3):
        print("wave augmentation:")
        for j in data:
            audio_file = j.strip().split(",")[0]
            label_file = j.strip().split(",")[1]
            output_file = sox_proceed(audio_file, aug_wav_path)
            roll_audio(output_file)
            f.write(output_file + "," + label_file + "\n")


# save label categories
label_kinds.sort()
with open(os.path.join(out_file, "label.json"), "w") as f:
    f.write('["_", ')
    for j in label_kinds:
        f.write('"{}", '.format(j))
    f.write('"{<unk>}", " "]')



