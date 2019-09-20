train:
python train.py --train-manifest /data2/data_B/5-fold/2/train_manifest.csv --val-manifest /data2/data_B/5-fold/2/test_manifest.csv --batch-size 16 --labels-path /data2/data_B/5-fold/2/label.json --checkpoint --cuda --rnn-type lstm --lr 5e-5 --save-folder /data2/data_B/5-fold/2/models --model-path /data2/data_B/5-fold/2/models/deepspeech_final.pt --hidden-size 512 --visdom --tensorboard --log-dir /data2/data_B/5-fold/2/visualize --log-params --spec-aug --epochs 150 --layernorm --gpu-num 1

test:
python test_iter.py --test-manifest /data2/data_B/5-fold/1/test_manifest.csv --gpu-num 0 --E2C /data2/data_B/preprocessed/E2C.json --C2E /data2/data_B/preprocessed/C2E.json --start-epoch 1 --end-epoch 6 --save-path /data2/data_B/5-fold/1/result/beam --beam-width 40 --lm-path /data2/data_B/5-fold/1/5.arpa --alpha 1.1 --beta 3 --cuda --decoder beam --model-path /data2/data_B/5-fold/1/model

pretrain:
python train.py --train-manifest /data2/data_B/5-fold/2/train_manifest.csv --val-manifest /data2/data_B/5-fold/2/test_manifest.csv --batch-size 16 --labels-path /data2/data_B/5-fold/2/label.json --checkpoint --cuda --rnn-type lstm --lr 5e-5 --save-folder /data2/data_B/5-fold/2/models --model-path /data2/data_B/5-fold/2/models/deepspeech_final.pt --hidden-size 512 --visdom --tensorboard --log-dir /data2/data_B/5-fold/2/visualize --log-params --spec-aug --epochs 150 --layernorm --gpu-num 1 --continue-from /data2/data_B/5-fold/2/models/deepspeech_59.pth
