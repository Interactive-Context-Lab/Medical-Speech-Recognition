# Change Log
### Version 1.0
#### Features
* Support for medical speech recognition mission
#### Areas of improvement
* Design a **new preprocessing method** to Medical Speech Corpus in Chinese (MEDICIC) dataset:
    
    * `split_sentance_from_audio.py` splits audio files from several nurses by using label file (.eaf).
    * `to_syllable.py` changes English text to syllable formation in each sentence and outputs `E2C.json` and `C2E.json`. (`E2C.json` is used to replace English words to Chinese words training a Chinese model; `C2E.json` is used to decode to the original English words during testing.)
    * `5-fold.py` seperates data into 5 folders and organizes audio, label and language model for each training set. Also, we augment the original audios in this script.

* Modify Deep Speech 2 model:
    
    * Use **3 layers on convolutional neural network** in MaskConv (2 layers original)
    * Change **batch normalization** to **layer normalization** in recurrent neural network layers and fully connected layer.

* Can train with or without the **augmented spectrogram data**
* New testing code for this medical dataset case

---

### Version 1.1
#### Features
* Provide a `mini_dataset` to implement the scripts
#### Areas of imporvement
* Remove the useless scripts
* Rewrite the `README.md` file to describe installation details, training and testing setiings
* Add `CHANGELOG.md` file to show the details

---

### Version 2.0
#### Features
* Support for medical speech recognition mission
* Use new ChiMeS dataset

#### Areas of improvement
* Design a **new preprocessing method** for Chinese Medical Speech Corpus (ChiMeS) dataset:
    * Change `5-fold.py` (in v1.0 and v1.1) to `create_train4_test1.py` or `create_manifest.py`, they generate manifest (w/ or w/o data augmentation) and organize audio, label and language model for training set. 

* Modify Deep Speech 2 model:
    
    * Rewrite **fine-tuning training** to **copy the parameters** to new model and get **new fully connected layer**.

