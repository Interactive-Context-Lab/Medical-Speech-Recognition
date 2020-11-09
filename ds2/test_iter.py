import argparse
import time
import numpy as np
import torch
from tqdm import tqdm
from data.data_loader import SpectrogramDataset, AudioDataLoader
from decoder import GreedyDecoder
from model import DeepSpeech, FinetuningModel
from opts import add_decoder_args, add_inference_args
import os
import json

def sep_seq(seq):
    temp = []
    is_eng_word = False
    word_temp = ""
    for c in seq:
        word_temp = word_temp + c
        if c == "{" or c == "}":
            is_eng_word = not is_eng_word
            if not is_eng_word:
                temp.append(word_temp)
                word_temp = ""
        elif not is_eng_word:
            temp.append(word_temp)
            word_temp = ""
    return temp




parser = argparse.ArgumentParser(description='DeepSpeech transcription')
parser = add_inference_args(parser)
parser.add_argument('--test-manifest', metavar='DIR',
                    help='path to validation manifest csv', default='/2TB/MEDICIC/A/baseline/test_manifest.csv')
parser.add_argument('--batch-size', default=16, type=int, help='Batch size for training')
parser.add_argument('--num-workers', default=4, type=int, help='Number of workers used in dataloading')
parser.add_argument('--verbose', action="store_true", help="print out decoded output and error of each sample")

# add by Willy
parser.add_argument('--gpu-num', default=0, type=int, help='the number of gpu to work')
parser.add_argument('--E2C', metavar='DIR',
                    help='path to E2C.json', default='/2TB/MEDICIC/BigA/A_Pretrain/spec_aug/E2C.json')
parser.add_argument('--C2E', metavar='DIR',
                    help='path to C2E.json', default='/2TB/MEDICIC/BigA/A_Pretrain/spec_aug/C2E.json')
parser.add_argument('--start-epoch', default=150, type=int, help='start epoch for test')
parser.add_argument('--end-epoch', default=150, type=int, help='end epoch for test')
parser.add_argument('--save-path', metavar='DIR',
                    help='path to save transcription result', default='/2TB/MEDICIC')

parser.add_argument('--finetune', dest='finetune', action='store_true',
                    help='Test the finetuning model')

no_decoder_args = parser.add_argument_group("No Decoder Options", "Configuration options for when no decoder is "
                                                                  "specified")
no_decoder_args.add_argument('--output-path', default=None, type=str, help="Where to save raw acoustic output")
parser = add_decoder_args(parser)
args = parser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_num)

if __name__ == '__main__':
    # args.cuda = True
    # args.verbose = True
    # args.decoder = "beam"
    for a in range(args.start_epoch, args.end_epoch + 1):
        from jiwer import wer
        t0 = time.time()
        model_path = os.path.join(args.model_path, "deepspeech_{}.pth".format(str(a)))
        torch.set_grad_enabled(False)

        if not args.finetune:
            model = DeepSpeech.load_model(model_path)

            if args.cuda:
                model.cuda()
            model.eval()

            labels = DeepSpeech.get_labels(model)
            C_labels = labels.copy()
            with open(args.E2C) as label_file:
                E2C = json.load(label_file)
            with open(args.C2E) as label_file:
                C2E = json.load(label_file)
            for i, v in enumerate(C_labels):
                if v in E2C:
                    C_labels[i] = E2C[v]

            audio_conf = DeepSpeech.get_audio_conf(model)
            audio_conf["spec_aug"] = False
            if args.decoder == "beam":
                from decoder_old import BeamCTCDecoder

                decoder = BeamCTCDecoder(C_labels, lm_path=args.lm_path, alpha=args.alpha, beta=args.beta,
                                         cutoff_top_n=args.cutoff_top_n, cutoff_prob=args.cutoff_prob,
                                         beam_width=args.beam_width, num_processes=args.lm_workers)
            elif args.decoder == "greedy":
                decoder = GreedyDecoder(labels, blank_index=labels.index('_'))
            else:
                decoder = None
        else:# Added by Angel******
            finetuning_model = FinetuningModel.load_model(model_path)

            if args.cuda:
                finetuning_model.cuda()
            finetuning_model.eval()

            labels = FinetuningModel.get_labels(finetuning_model)
            C_labels = labels.copy()
            with open(args.E2C) as label_file:
                E2C = json.load(label_file)
            with open(args.C2E) as label_file:
                C2E = json.load(label_file)
            for i, v in enumerate(C_labels):
                if v in E2C:
                    C_labels[i] = E2C[v]

            audio_conf = FinetuningModel.get_audio_conf(finetuning_model)
            audio_conf["spec_aug"] = False
            if args.decoder == "beam":
                from decoder_old import BeamCTCDecoder

                decoder = BeamCTCDecoder(C_labels, lm_path=args.lm_path, alpha=args.alpha, beta=args.beta,
                                         cutoff_top_n=args.cutoff_top_n, cutoff_prob=args.cutoff_prob,
                                         beam_width=args.beam_width, num_processes=args.lm_workers)
            elif args.decoder == "greedy":
                decoder = GreedyDecoder(labels, blank_index=labels.index('_'))
            else:
                decoder = None
        target_decoder = GreedyDecoder(labels, blank_index=labels.index('_'))
        test_dataset = SpectrogramDataset(audio_conf=audio_conf, manifest_filepath=args.test_manifest, labels=labels,
                                          normalize=True)
        test_loader = AudioDataLoader(test_dataset, batch_size=args.batch_size,
                                      num_workers=args.num_workers)
        total_cer, total_wer, num_tokens, num_chars = 0, 0, 0, 0
        output_data = []
        with open(os.path.join(args.save_path, str(a) + ".txt"), 'w') as f:
            for i, (data) in tqdm(enumerate(test_loader), total=len(test_loader)):
                inputs, targets, input_percentages, target_sizes = data
                input_sizes = input_percentages.mul_(int(inputs.size(3))).int()
                # unflatten targets
                split_targets = []
                offset = 0
                for size in target_sizes:
                    split_targets.append(targets[offset:offset + size])
                    offset += size

                if args.cuda:
                    inputs = inputs.cuda()

                if not args.finetune:
                    out, output_sizes = model(inputs, input_sizes)
                else:    # Added by Angel******
                    out, output_sizes = finetuning_model(inputs, input_sizes)

                if decoder is None:
                    # add output to data array, and continue
                    output_data.append((out.numpy(), output_sizes.numpy()))
                    continue
                target_strings = target_decoder.convert_to_strings(split_targets)
                decoded_output, _ = decoder.decode(out.data, output_sizes.data)
                for x in range(len(target_strings)):
                    transcript, reference = decoded_output[x][0], target_strings[x][0]
                    for i in C2E:
                        transcript = transcript.replace(i, C2E[i])
                    wer_inst = decoder.wer(transcript, reference)
                    # cer_inst = decoder.cer(transcript, reference)
                    ref_sep = sep_seq(reference)
                    trans_sep = sep_seq(transcript)
                    if len(trans_sep) == 0:
                        cer_inst = len(ref_sep)
                    else:
                        cer_inst = round(wer(ref_sep, trans_sep) * len(ref_sep))
                    total_wer += wer_inst
                    total_cer += cer_inst
                    num_tokens += 1
                    num_chars += len(ref_sep)

                    print("Ref:", reference.lower())
                    print("Hyp:", transcript.lower())
                    print("WER:", float(wer_inst) / 1, "CER:", float(cer_inst) / len(ref_sep), "\n")
                    f.write("Ref:" + reference.lower() + '\n')
                    f.write("Hyp:" + transcript.lower() + '\n')
                    f.write("WER:" + str(float(wer_inst) / 1) + "CER:" + str(float(cer_inst) / len(ref_sep)) + "\n")

            if decoder is not None:
                wer = float(total_wer) / num_tokens
                cer = float(total_cer) / num_chars

                print('Test Summary \t'
                      'Average WER {wer:.3f}\t'
                      'Average CER {cer:.3f}\t'.format(wer=wer * 100, cer=cer * 100))
                f.write('Test Summary \t' +
                      'Average WER {wer:.3f}\t'.format(wer=wer * 100) +
                      'Average CER {cer:.3f}\t'.format(cer=cer * 100) + '\n' +
                      'Time:{:.3f}\n'.format(time.time()-t0))
            else:
                np.save(args.output_path, output_data)
