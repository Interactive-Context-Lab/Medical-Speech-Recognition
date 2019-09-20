"""
Step 1 of pre-processing
cut each sentences in origin audio of nursing handover
the format of labeled audio is:

file_dir ──┬── sub_file[0] ──┬── XXX_01  ──┬── XXX.wav
           ├── sub_file[1]   ├── XXX_02    └── XXX.eaf
           └── ...           └── ...

All the output are stored in preprocessed_dir,
the processed audio and label of each sentence, stored in "wave" directory and "label" directory separately,
and the path of all processed data is list in "manifest.csv", in where each line is the audio and label path of each data.
Also, each sentence's information is store in all_label.txt, including the processed audio file name, start time, end time and label.


:file_dir: input audio directory
:sub_file: list of the sub-file directory in file_dir
:preprocessed_dir: directory that stores processed data
"""

import os
import wave
import xml.etree.cElementTree as ET
import numpy as np


file_dir = "/data2/data_B/labeled_audio"
sub_file = ["20190522","20190524","20190530","20190605"]
preprocessed_dir = "/data2/punctuation_B/preprocessed"

def CUT_ANOTED(XML_FILE, WAVE_FILE):
    """
    Cut sentences in WAVE_FILE by XML_FILE
    :param XML_FILE: .eaf file
    :param WAVE_FILE: Wave file corresponding to XML_FILE
    :return: a dictionary,  key of dictionary is sentence ID and value of dictionary is a tuple including label, wave data, start time and end time of WAVE_FILE
             other return value is the wave format of WAVE_FILE
    """

    # parse XML_FILE to get ID, start time, and end time of each sentence
    tree = ET.ElementTree(file=XML_FILE)
    time_slots = {}
    for elem in tree.iter(tag='TIME_SLOT'):
        time_slots[elem.attrib["TIME_SLOT_ID"]] = elem.attrib["TIME_VALUE"]

    # read data and format of WAVE_FILE
    f = wave.open(WAVE_FILE, 'r')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    wave_file = f.readframes(nframes)
    f.close()
    wave_file = np.fromstring(wave_file, dtype=np.short)

    # cut each sentence and store in "annote_result"
    annote_result = {}
    for elem in tree.iter(tag='ALIGNABLE_ANNOTATION'):
        annote_ID, annote_start, annote_end = elem.attrib["ANNOTATION_ID"], elem.attrib["TIME_SLOT_REF1"], elem.attrib["TIME_SLOT_REF2"]
        label = elem[0].text
        annote_audio = wave_file[int(time_slots[annote_start]) * 16 : int(time_slots[annote_end]) * 16]
        annote_result[annote_ID.replace("a","")] = (label, annote_audio, time_slots[annote_start], time_slots[annote_end])

    return annote_result, nchannels, sampwidth, framerate, nframes


target_audio_file = os.path.join(preprocessed_dir, "wave")
if not os.path.exists(target_audio_file): os.makedirs(target_audio_file)
target_label_file = os.path.join(preprocessed_dir, "label")
if not os.path.exists(target_label_file): os.makedirs(target_label_file)

# traverse all nursing handover file in each sub_file
for each_dir in sub_file:
    cur_path = os.path.join(file_dir,each_dir)
    for file in os.listdir(cur_path):
        sub_dir = os.path.join(cur_path,file)
        if os.path.isdir(sub_dir):
            sub_files = os.listdir(sub_dir)
            wav_file = None
            label_file = None
            for sub_file in sub_files:
                if sub_file.endswith(".wav"):
                    wav_file = sub_file
                elif sub_file.endswith(".eaf"):
                    label_file = sub_file
            # if the file have wave file and .eaf label file, use function{CUT_ANOTED} to cut each sentence
            if wav_file != None and label_file != None:
                annote_result, nchannels, sampwidth, framerate, nframes = CUT_ANOTED(os.path.join(sub_dir,label_file),os.path.join(sub_dir,wav_file))
                print("{}".format(file))
                # store wave and label of each sentence
                for k,v in annote_result.items():
                    if v[0] != None:
                        label_processed = v[0].replace(" ","").replace("、","，").replace("，","，").replace("。","，").replace(",","，").replace(".","").replace("/","").lower()
                        if label_processed[-1] == "，":
                            label_processed = label_processed[:-1]
                        with open(os.path.join(os.path.join(preprocessed_dir), "all_label.txt") ,'a', encoding="utf-8") as f:
                            f.write("{}_{}".format(file,k) + "\t" + v[2] + "\t" + v[3] + "\t" + label_processed + '\n')
                        with open(os.path.join(os.path.join(preprocessed_dir), "manifest.csv") ,'a', encoding="utf-8") as f:
                            f.write("{},{}\n".format(os.path.join(target_audio_file, "{}_{}.wav".format(file,k)), os.path.join(target_label_file, "{}_{}.txt".format(file,k))))
                        with open(os.path.join(target_label_file, "{}_{}.txt".format(file,k)), "w", encoding="utf-8") as f:
                            f.write(label_processed)
                        f = wave.open(os.path.join(target_audio_file, "{}_{}.wav".format(file,k)), "wb")
                        f.setnchannels(nchannels)
                        f.setsampwidth(sampwidth)
                        f.setframerate(framerate)
                        f.writeframes(v[1].tostring())
                        f.close()
