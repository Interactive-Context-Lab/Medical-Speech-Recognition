Train:
python train.py --train-manifest /dataA/train_manifest.csv --val-manifest /dataA/test_manifest.csv --batch-size 16 --labels-path /dataA/label.json --checkpoint --cuda --rnn-type lstm --lr 5e-5 --save-folder /dataA/models --model-path /dataA/models/deepspeech_final.pth --hidden-size 512 --visdom --tensorboard --log-dir /dataA/visualize --log-params --epochs 150 --layernorm --spec-aug

->Continue to train model from .pth:
python train.py --train-manifest /dataA/train_manifest.csv --val-manifest /dataA/test_manifest.csv --batch-size 16 --labels-path /dataA/label.json --checkpoint --cuda --rnn-type lstm --lr 5e-5 --save-folder /dataA/models --model-path /dataA/models/deepspeech_final.pth --hidden-size 512 --visdom --tensorboard --log-dir /dataA/visualize --log-params --epochs 150 --layernorm --continue-from /pretrain_models/deepspeech_10.pth --spec-aug

->Finetuning
python train.py --train-manifest /dataA/train_manifest.csv --val-manifest /dataA/test_manifest.csv --batch-size 16 --labels-path /dataA/label.json --checkpoint --cuda --rnn-type lstm --lr 5e-5 --save-folder /dataA/models --model-path /dataA/models/deepspeech_final.pth --hidden-size 512 --visdom --tensorboard --log-dir /dataA/visualize --log-params --epochs 150 --layernorm --continue-from /pretrain_models/deepspeech_10.pth --spec-aug --finetune

->Continue to train finetuning model
python train.py --train-manifest /dataA/train_manifest.csv --val-manifest /dataA/test_manifest.csv --batch-size 16 --labels-path /dataA/label.json --checkpoint --cuda --rnn-type lstm --lr 5e-5 --save-folder /dataA/models --model-path /dataA/models/deepspeech_final.pth --hidden-size 512 --visdom --tensorboard --log-dir /dataA/visualize --log-params --epochs 150 --layernorm --continue-from /pretrain_models/deepspeech_10.pth --spec-aug --finetune-continue

Test:
->Beam
python test_iter.py --test-manifest /dataA/test_manifest.csv --E2C /dataA/E2C.json --C2E /dataA/C2E.json --save-path /dataA/results/beam --beam-width 40 --lm-path /dataA/5.arpa --alpha 1.1 --beta 3 --cuda --decoder beam --model-path /dataA/models
 --start-epoch 1 --end-epoch 150 

->Greedy
python test_iter.py --test-manifest /dataA/test_manifest.csv --E2C /dataA/E2C.json --C2E /dataA/C2E.json --save-path /dataA/results/greedy --cuda --decoder greedy --model-path /dataA/models --start-epoch 1 --end-epoch 150 




