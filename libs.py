# coding=UTF-8
# /*************************************************
# Copyright:
# Author:XYJ
# Date:
# Description: 
# **************************************************/
import numpy as np
import time
import os
import traceback

DATAPATH = 'data/'
if not os.path.exists(DATAPATH):
    os.mkdir(DATAPATH)


def test(*args, **kwarg):
    pass


def get_time_str():
    return time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))


def write_to_csv(fname, l_, d2_flag=True, row_to_col=True):
    import csv
    with open(fname, 'wb') as csvfile:
        if row_to_col:
            l_ = np.array(l_).transpose()
        if d2_flag:
            spamwriter = csv.writer(csvfile)
            for i in range(len(l_)):
                spamwriter.writerow(l_[i])
        else:
            for i in range(len(l_)):
                csvfile.write(str(l_[i]) + '\n')


if __name__ == '__main__':
    pass
