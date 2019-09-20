import speech_recognition
import time


r = speech_recognition.Recognizer()

with open("/home/ee303/Documents/deepspeech.pytorch/500_manifest/ATCOSIM_clear_test.csv") as f:
    files = f.readlines()

files = [a.strip().split(",") for a in files]
a = 0
with open("/home/ee303/Documents/deepspeech.pytorch/results/ATCOSIM/google.txt", 'a') as result_file:
    for each_wav in files:
        a = a + 1
        print(a)
        wav_path = each_wav[0]
        file_name = wav_path.split("/")[-1].split(".")[0]
        label_path = each_wav[1]

        with open(label_path) as f:
            label = f.readlines()[0]

        print(file_name)
        print(label)

        result_file.write(file_name + '\n')
        result_file.write(label + '\n')

        with speech_recognition.AudioFile(wav_path) as source:
            audio = r.record(source)

        try:
            recoged = r.recognize_google(audio, language="en-US")
            print(recoged)
            result_file.write(recoged + '\n')
            time.sleep(1)

        except:
            print("UnknownValueError")
            result_file.write('\n')
            with open("/home/ee303/Documents/deepspeech.pytorch/results/ATCOSIM/err.txt", 'w') as err:
                err.write(file_name + '\n')
            time.sleep(5)



