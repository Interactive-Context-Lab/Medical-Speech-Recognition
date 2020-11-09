# Change Log
### Version 2.0
#### Features
* Support for medical speech recognition mission
#### Areas of improvement
* Design a **new preprocessing method** to Chinese Medical Speech Corpus (ChiMeS) dataset:
    
    * `split_sentance_from_audio.py` splits audio files from several nurses by using label file (.eaf).
    * `to_syllable.py` changes English text to syllable formation in each sentence and outputs `E2C.json` and `C2E.json`. (`E2C.json` is used to replace English words to Chinese words training a Chinese model; `C2E.json` is used to decode to the original English words during testing.)
    * `create_train4_test1.py` or `create_manifest.py` generates manifest (w/ or w/o data augmentation) and organizes audio, label and language model for training set. 


* Modify Deep Speech 2 model:
    
    * Rewrite **fine-tuning training** to **copy the parameters** to new model and get **new fully connected layer**.

