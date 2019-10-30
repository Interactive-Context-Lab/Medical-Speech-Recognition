# Medical Speech Recognition
本網站的程式經由參考並修改 https://github.com/SeanNaren/deepspeech.pytorch 的內容獲得。
# 安裝
1. 安裝 [pytorch](https://github.com/pytorch/pytorch#installation)

2. 安裝 [Warp-CTC](https://github.com/SeanNaren/warp-ctc)

3. 若預測時需要使用 beam search decoder，需安裝 [ctcdecoder](https://github.com/parlance/ctcdecode.git)

4. 若要引入語言模型協助預測，需安裝 [KenLm](https://github.com/kpu/kenlm)

5. 安裝 pytorch audio:
```
sudo apt-get install sox libsox-dev libsox-fmt-allg
git clone https://github.com/pytorch/audio.git
cd audio
python setup.py install
```
6. 安裝其餘所需模組:
```
pip install -r requirements.txt
```

# 預處理

此網址提供一預處理程式，此程式針對 Medical Speech Corpus in Chinese(MEDICIC) 資料庫進行預處理，經處理後將分為 5-fold 以進行交叉驗證並便於後續的訓練與測試。

預處理共分為三個程式檔案。

1. split_sentence_from_audio.py:
將護理師完整念誦一個交班的的語音檔，透過標註檔 .eaf 檔切分為一句句的音檔與對應的文字內容。

2. to_syllable.py
將各句話的文字內容中，英文部分標註為 音節 (syllable) 的標註方式。

3. 5-fold.py
將所有的資料分為 5-fold、並為各個 fold 分別產生增量的音檔以及各自訓練集句子的語言模型。

# 訓練
#### 資料集
目前僅支援 Medical Speech Corpus in Chinese(MEDICIC) 資料庫的預處理與訓練、測試。

用於訓練的檔案格式為 .csv 檔，檔案內每行的內容為一個音檔的路徑與對應的文字檔路徑，如下所示：
```
/dataset/audio/audio_1.wav,/dataset/label/label_1.txt
/dataset/audio/audio_2.wav,/dataset/label/label_2.txt
...
```
#### 訓練模型
訓練的命令如下所示，所需的檔案皆可於預處理程式的輸出中獲得：
```
python train.py --train-manifest /dataset/train_manifest.csv --val-manifest /dataset/test_manifest.csv --labels-path /dataset/label.json --batch-size 16 --epochs 100 --lr 5e-5 --rnn-type lstm --hidden-size 512 --layernorm --spec-aug --cuda --checkpoint --save-folder /dataset/models --model-path /dataset/models/deepspeech_final.pt
```
上述參數中:
* train-manifest : 訓練集的 .csv 檔之路徑
* val-manifest : 驗證集的 .csv 檔之路徑
* labels-path : 字種類的 .json 檔之路徑
* batch-size : 批量大小
* epoch : 迭帶次數
* lr : learning rate 學習率
* rnn-type : 模型使用之 RNN 的類型，可選 RNN、LSTM、GRU
* hidden-size : RNN hidden unit 的大小
* layernorm : 對 RNN 使用 layer normalization，若無輸入則使用 Batch normalization
* spec-aug : 使用頻譜增量 Spectaugmentation
* cuda : 使用 GPU 進行訓練
* checkpoint : 每個 epoch 都儲存當前之模型權重
* save-folder : 模型權重儲存之資料夾路徑
* model-path : 於驗證集測試獲得之最佳權重的儲存路徑

可使用 python train.py -\-help 獲得更多的參數及選項

# 測試
測試階段將訓練時所儲存的各個 epoch 的模型權重檔對測試集的語音進行預測，並與ground truth 計算 Character error rate (CER) 作為評判模型好壞的標準。

```
python test_iter.py --test-manifest /dataset/test_manifest.csv --E2C /dataset/E2C.json --C2E /dataset/C2E.json --model-path /dataset/model --start-epoch 1 --end-epoch 100 --save-path /dataset/result/beam --decoder beam --lm-path /dataset/LM.arpa --beam-width 40 --alpha 1.1 --beta 3 --cuda
```

* test-manifest : 測試集 .csv 檔之路徑
* E2C, C2E : 用於將英文音節轉換為中文字的 .josn 檔
* model-path : 模型權重所儲存的目錄
* start-epoch, end-epoch : 需要測試的起始與結束之 epoch
* save-path : 測試結果儲存之目錄
* decoder : 可選擇 greedy (greedy decoder) 或是 beam (beam search decoder)，若選擇 beam 則需要下列參數:
	* lm-path : 語言模型 (langauge model) 的路徑
	* beam-width, alpha, beta : beam search decoder 的光束寬度以及引用語言模型的參數
* cuda : 使用 GPU 進行測試

可使用 python test_iter.py -\-help 獲得更多的參數及選項

# Demo影片
[![](http://img.youtube.com/vi/AQ78hGx3usc/0.jpg)](http://www.youtube.com/watch?v=AQ78hGx3usc "")
