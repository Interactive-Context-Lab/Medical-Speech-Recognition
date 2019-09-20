# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
import numpy
import os
import numpy as np

def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.
    Main algorithm used is dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8).reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitute = d[i - 1][j - 1] + 1
                insert = d[i][j - 1] + 1
                delete = d[i - 1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d


def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0:
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x - 1][y - 1] and r[x - 1] == h[y - 1]:
            list.append("e")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y - 1] + 1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x - 1][y - 1] + 1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]


def alignedPrint(list, r, h, result):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.

    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
        result -> the rate calculated based on edit distance.
    '''
    print
    "REF:",
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print
            " " * (len(h[index])),
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                print
                r[index1] + " " * (len(h[index2]) - len(r[index1])),
            else:
                print
                r[index1],
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print
            r[index],
    print
    print
    "HYP:",
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print
            " " * (len(r[index])),
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print
                h[index2] + " " * (len(r[index1]) - len(h[index2])),
            else:
                print
                h[index2],
        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print
            h[index],
    print
    print
    "EVA:",
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print
            "D" + " " * (len(r[index]) - 1),
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print
            "I" + " " * (len(h[index]) - 1),
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print
                "S" + " " * (len(r[index1]) - 1),
            else:
                print
                "S" + " " * (len(h[index2]) - 1),
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print
            " " * (len(r[index])),
    print
    print
    "WER: " + result


def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split()) 
    """
    # build the matrix
    d = editDistance(r, h)

    # find out the manipulation steps
    list = getStepList(r, h, d)

    # print the result in aligned way
    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.4f" % result) + "%"
    print(result)

    return float(d[len(r)][len(h)]), len(r)
    # alignedPrint(list, r, h, result)


if __name__ == '__main__':
    from_file = u"/home/ee303/Documents/deepspeech.pytorch/results/ATCOSIM/google.txt"

    with open(from_file, 'r') as f:
        from_content = f.readlines()
    from_content = [a.strip() for a in from_content]



    add_up = []
    add_down = []

    result_list = []
    CER_list = []

    with open("/home/ee303/Documents/deepspeech.pytorch/results/ATCOSIM/google_CER.txt", 'w') as f:
        for i in range(0, len(from_content), 3):
            print(from_content[i])
            print(from_content[i+1])
            print(from_content[i+2])
            up, down = wer(list(from_content[i+1]), list(from_content[i+2]))
            add_up.append(up)
            add_down.append(down)
            CER_list.append(up/down)
            print(up/down)
            f.write(from_content[i] + '\n')
            f.write(from_content[i+1] + '\n')
            f.write(from_content[i+2] + '\n')
            f.write(str(up/down) + '\n')

        print("AVERAGE : " + str(np.array(CER_list).mean()))
        f.write("AVERAGE : " + str(np.array(CER_list).mean()))


        # with open(filename.split(".")[0] + '_CER.txt', 'a') as f:
        #     f.write(results[i] + '\n' + results[i+1] + '\n' + str(up / down) + '\n')

    print(np.array(CER_list).mean())
    # print('\n \n ALL CER:%.4f' % (numpy.sum(list(add_up.values())) / numpy.sum(list(add_down.values())) * 100))


    # # with open(filename.split(".")[0] + '_CER.txt', 'a') as f:
    # #     f.write("\nALL\nCER:" + "%.4f" % (add_up / add_down * 100) + "\n")
    # # print("ALL\nCER:","%.4f" % (add_up / add_down * 100))
    #
    # with open("/home/ee303/Documents/deepspeech.pytorch/new_lstm/beam_result/25.txt") as f:
    #     results = f.readlines()
    # results = [a.strip().split(":")[1] for a in results]
    #
    # add_up = {}
    # add_down = {}
    #
    # result_list = {}
    # CER_list = {}
    #
    #
    # for i in range(0, len(results), 3):
    #     print(results[i])
    #     print(results[i+1])
    #     up, down = wer(list(results[i]), list(results[i + 1]))
    #     if results[i][0] not in add_up:
    #         add_up[results[i][0]] = 0
    #         add_down[results[i][0]] = 0
    #         result_list[results[i][0]] = []
    #         CER_list[results[i][0]] = []
    #     add_up[results[i][0]] += up
    #     add_down[results[i][0]] += down
    #     result_list[results[i][0]].append(results[i] + '\n' + results[i+1] + '\n')
    #     CER_list[results[i][0]].append(up/down)
    #
    #
    #     # with open(filename.split(".")[0] + '_CER.txt', 'a') as f:
    #     #     f.write(results[i] + '\n' + results[i+1] + '\n' + str(up / down) + '\n')
    #
    # print('\n \n ALL CER:%.4f' % (numpy.sum(list(add_up.values())) / numpy.sum(list(add_down.values())) * 100))
    #
    #
    # # with open(filename.split(".")[0] + '_CER.txt', 'a') as f:
    # #     f.write("\nALL\nCER:" + "%.4f" % (add_up / add_down * 100) + "\n")
    # # print("ALL\nCER:","%.4f" % (add_up / add_down * 100))