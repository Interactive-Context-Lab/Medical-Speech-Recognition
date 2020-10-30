# Medical Speech Recognition Model
* [Overview](#Overview)
* [Intallation](#Intallation)
    * [Hardware Information](#Hardware-Information)
    * [Software Requirements](#Software-Requirements)
    * [Install Dependencies](#Install-Dependencies)
* [Dataset](#Dataset)
* [Preprocessing](#Preprocessing)
* [Training](#Training)
* [Testing](#Testing)


## Overview
#### The main features:
* In this repository, we have developed a medical speech recognition model for recording speeches during nursing shift handovers.
* A nursing handover dataset has been collected. And this dataset contains labeled audio speeches recorded from nursing stations.
#### Base:
* The model is based on [Deep Speech 2](https://github.com/SeanNaren/deepspeech.pytorch), and the **changes are in [CHANGELOG.md](CHANGELOG.md)**, and you can check it for all the details.


## Intallation
### Hardware Information
These are the hardware inforamation we used to train or test our model.
* CPU: Intel Core i7-8700K
* GPU: NVIDIA GTX 1080TI
* RAM: 24GB
### Software Requirements
These are software and framework versions.
* OS: **Ubuntu 16.04 (Note: Not support for windows)**
* CUDA: 9.0
* cuDNN: 7.1
* Python: 3.6
* Pytorch: 1.1.0
### Install Dependencies
1. **Make sure to install [pytorch v1.1.0](https://github.com/pytorch/pytorch#installation)**, for example (anaconda):
    ```
    conda install pytorch==1.1.0 torchvision==0.3.0 cudatoolkit=9.0 -c pytorch
    ```
2. Install **requirements**:
    ```
    pip install -r requirements.txt
    ```
    
3. Install **warp-CTC**:
    
    Clone from github and install:
    ```
    git clone https://github.com/SeanNaren/warp-ctc.git
    cd warp-ctc
    mkdir build; cd build
    cmake ..
    make
    ```
    Install pytorch binding:
    ```
    cd pytorch_binding
    python setup.py install
    ```
    Github link: https://github.com/SeanNaren/warp-ctc
    
    Note: If there is no `_warp_ctc` module, here is the installation issue: https://github.com/SeanNaren/warp-ctc/pull/31
4. Install **ctcdecoder**:
    
    This module includes **beam search decoder** for testing your model **if you need it.**
    
    Clone from github and install: 
    ```
    git clone --recursive https://github.com/parlance/ctcdecode.git
    cd ctcdecode
    python setup.py install
    ```
    Github link: https://github.com/parlance/ctcdecode .
5. Install **KenLm**:
    
    You can use this language model for prediction.
    
    C++ builder:
    ```
    sudo apt install build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev
    ```
    Clone from gihub and install:
    ```
    git clone https://github.com/kpu/kenlm.git
    cd kenlm
    mkdir -p build
    cd build
    cmake ..
    make -j 4
    ```
    Install python module:
    ```
    cd kenlm
    python setup.py install
    ```
    Github link: https://github.com/kpu/kenlm.
7. Install **pytorch audio** from pytorch.org by following:
    ```
    sudo apt-get install sox libsox-dev libsox-fmt-all
    pip install http://download.pytorch.org/whl/torchaudio-0.2-cp36-cp36m-linux_x86_64.whl
    ```


## Dataset
This model only supports for **Medical Speech Corpus in Chinese (MEDICIC)** dataset for training and testing. We provide a `mini_dataset` to make sure you can use this baseline. And if you are using other dataset, you have to reconstruct the dataset directories refer to the following descriptions.

Note:
We use manifest file in `.csv` formation. In this file, each row contains paths of audio file and corresponding text file. For example:
```
/dataset/audio/audio_1.wav,/dataset/label/label_1.txt
/dataset/audio/audio_2.wav,/dataset/label/label_2.txt
...
```


## Preprocessing
In the `preprocess/` directory, we provide a preprocessing code. This code will preprocess the raw dataset in specific structure (you can refer to `mini_dataset`). After processing, it will output dataset for training and testing.


There are three steps to preprocess dataset follow by these three scripts, and **you have to modify the directory inside each script to fit your dataset**.

* `split_sentence_from_audio.py` splits audio files from several nurses by using label file (.eaf). And  outputs are the splited audio files corresponding to the sentences in label files.
    * Inputs:
        
        ```
        file_dir/ ─┬─ sub_file[0]/ ─┬─ XXX_01/ ─┬─ XXX.wav
                   ├─ sub_file[1]/  ├─ XXX_02/  └─ XXX.eaf
                   └─ ...           └─ ...
        ```
        
    * Outputs:
        
        ```
        preprocessed/ ─┬─ label/ ─── XXX.txt
                       ├─ wave/ ─── XXX.wav
                       ├─ all_label.txt
                       └─ manifest.csv
        ```
* `to_syllable.py` changes English text to syllable formation in each sentence and outputs `E2C.json` and `C2E.json`. 
    * Input: `preprocessed/manifest.csv`, `word2syllable.txt`
    * Output: `syllable_manifest.csv`, `E2C.json`, `C2E.json`
        
        * `E2C.json` is used to replace English words to Chinese words training a Chinese model.
        * `C2E.json` is used to decode to the original English words during testing.

* `5-fold.py` seperates data into 5 folders and organizes audio, label and language model for each training set. Also, we augment the original audios in this script.
    * Input: `syllable_manifest.csv`, `E2C.json`, `kenlm language model`
    * Output:
    
        ```
        5fold/ ─┬─ 1/ ─┬─ augmet/ ─── XXX.wav
                ├─ 2/  ├─ label.json
                ├─ 3/  ├─ train_manifest.csv
                ├─ 4/  ├─ test_manifest.csv
                └─ 5/  ├─ txt4LM.txt # for langauge model
                       └─ 5.arpa # for language model
        ```
        
<!--* Choose one of them:
`create_train4_test1.py` generates training manifest file (with data augmentation), testing manifest, language model, and label categories.
`create_manifest.py` This script generates manifest (without data augmentation), language model, and label categories. -->

## Trainning
The following is the command line for training `mini_dataset` example:
```
python train.py --train-manifest ../mini_dataset/5fold/1/train_manifest.csv --val-manifest ../mini_dataset/5fold/1/test_manifest.csv --labels-path ../mini_dataset/5fold/1/label.json --batch-size 16 --epochs 150 --lr 5e-5 --rnn-type lstm --hidden-size 512 --layernorm --spec-aug --cuda --checkpoint --save-folder ../mini_dataset/5fold/1/models --model-path ../mini_dataset/5fold/1/models/deepspeech_final.pth
```
hyper-parameters:
* **train-manifest**: path to training set in .csv formation
* **val-manifest**: path to validation set in .csv formation
* **labels-path**: path to label categories in .json formation
* **batch-size**: for minibatch training
* **epoch**: number of itration for whole dataset
* **lr**: learning rate
* **rnn-type**: type of RNN model, including RNN, LSTM and GRU
* **hidden-size**: size of RNN hidden unit
* **layernorm**: normalization of RNN layers, default: batch normalization
* **spec-aug**: spectrogram augmentation
* **cuda**: GPU for training
* **checkpoint** : save model weight every epoch
* **save-folder** : path to save the weight
* **model-path** : path to the best weight from validation

Use `python /rain.py -\-help` to get more parameters and options.

Note: You will obtain **model file (.pth)** in your `model-path` every epoch and also a **final model** which is the best model.

## Testing
In testing, `test_iter.py` makes prediction and calculates CER and WER (standards to evaluate model) on every models from training process. Command line for `mini_dataset` example:
```
python test_iter.py --test-manifest ../mini_dataset/5fold/1/test_manifest.csv --E2C ../mini_dataset/preprocessed/E2C.json --C2E ../mini_dataset/preprocessed/C2E.json --model-path ../mini_dataset/5fold/1/models --start-epoch 1 --end-epoch 100 --save-path ../mini_dataset/5fold/1/ --decoder beam --lm-path ../mini_dataset/5fold/1/5.arpa --beam-width 40 --alpha 1.1 --beta 3 --cuda
```

* **test-manifest**: path to testing set in .csv formation
* **E2C, C2E**: path to .json which are used to convert English syllables between Chinese characters
* **model-path**: path to model weight
* **start-epoch, end-epoch** : start epoch index, end epoch index
* **save-path**: path to save the testing results. **You have to create a path by yourself.**
* **decoder**: choose one of methods to decode
    * **greedy (greedy decoder)**
    * **beam (beam search decoder)**: If you use beam to be the decoder, you have to set the following parameters.
        * **lm-path**: path to langauge model (have to use .arpa file generate by kenlm -**Bug to fix**)
        * **beam-width**, **alpha**, **beta**
* **cuda**: use GPU for testing

Use `python test_iter.py -\-help` to get more parameters and options.



## Demo
[![影片連結](http://img.youtube.com/vi/AQ78hGx3usc/0.jpg)](http://www.youtube.com/watch?v=AQ78hGx3usc "")
