__author__ = 'Administrator'

from matplotlib import pyplot
import copy
import os
import numpy as np

def isnum(ch):
    return 48 <= ord(ch) <= 57


def read_file_into_matrix_datas(filename):
    f = file(filename, 'r')
    lines = f.readlines()
    datas = []

    for line in lines:
        s = ''
        col = 0
        for j in line:
            if isnum(j) or j == '.' or j == '-' or j == 'e':
                s += j
            elif s != '':
                try:
                    if '.' in s:
                        datas[col].append(float(s))
                    else:
                        datas[col].append(int(s))
                except:
                    datas.append([])
                    if '.' in s:
                        datas[col].append(float(s))
                    else:
                        datas[col].append(int(s))
                col += 1
                s = ''
    return datas


def listfile(path='', flag='file'):
    """
    flag has the choices:
    file, dir, all
    """
    if path == '':
        path = '.'
    elif path[-1] not in ['\\', '/']:
        path += '/'
    files = []
    if flag == 'file':
        fs = os.listdir(path)
        for f in fs:
            if not os.path.isdir(f):
                files.append(f)
    return files

# step = 0.05
# ideal = [5.0+round(0.05*i, 2) for i in range(step_num)]
# data = open('ch2_50ps.csv', 'r').readlines()
fmat = 'png'
files = listfile()
print('choose file:')
for i in range(len(files)):
    print i, '---', files[i]
while True:
    index = input('input index:')
    datas = read_file_into_matrix_datas(files[index])
    dat = []
    for i in datas:
        dat += i
    step_num = len(dat)

    dat_origin = np.array(dat)
    # dat_origin *= 10e8
    step_sum = dat_origin[-1] - dat_origin[0]
    # print step_sum, dat_origin
    # sum_ = 0
    # for i in range(1, len(dat_origin)):
    #     sum_ += 1
    #     step_sum += dat_origin[i] - dat_origin[i-1]
    real_step = round(step_sum / (step_num - 1), 6)
    # print(real_step, step_num - 1)

    real_ideal = [round(dat_origin[0]+round(real_step*i, 6), 6) for i in range(step_num)]

    steps = range(step_num)
    for i in range(step_num):
        dat.insert(step_num - i, dat[step_num - i - 1])
        steps.insert(step_num - i, steps[step_num - i - 1])

    steps.pop(0)
    steps.pop(0)
    dat.pop(0)
    dat.pop()
    # print(steps)
    # print(dat)
    pyplot.plot(steps, dat)
    pyplot.ylim(min(dat), max(dat))
    pyplot.xlabel('Input delay value n')
    pyplot.ylabel('Delta delay time (ns)')
    pyplot.grid()
    pyplot.savefig('steps.%s'%fmat, dpi=300, format=fmat)
    pyplot.clf()

    # gap_step_num = int(round(abs(dat[0] - real_ideal[0])/real_step))
    # if dat_origin[0] < real_ideal[0]:
    #     for i in range(len(dat_origin)):
    #         dat_origin[i] += gap_step_num * real_step
    # elif dat_origin[0] > real_ideal[0]:
    #     for i in range(len(dat_origin)):
    #         dat_origin[i] -= gap_step_num * real_step

    # DNL = |[(VD+1- VD)/VLSB-IDEAL - 1] |, 0 < D < 2N - 2
    DNL = []
    for i in range(len(dat_origin)):
        if i == 0:
            DNL.append(0.0)
        else:
            DNL.append((dat_origin[i] - dat_origin[i-1])/real_step - 1)

    # INL = | [(VD - VZERO)/VLSB-IDEAL] - D , 0 < D < 2N-1
    INL = []
    for i in range(len(DNL)):
        INL.append(sum(DNL[:i+1]))
    print 'step=%f'%real_step
    print 'data:', dat_origin
    # print(real_ideal)
    print 'steps:', [round(dat_origin[i] - dat_origin[i-1], 6) for i in range(1,len(dat_origin))]
    # print([round(real_ideal[i] - real_ideal[i-1], 6) for i in range(1,len(real_ideal))])
    print('max&min of DNL:', max(DNL), min(DNL))
    print('max&min of INL:', max(INL), min(INL))
    pyplot.plot(DNL)
    pyplot.xlabel('Input value n')
    pyplot.ylabel('DNL(LSB)')
    pyplot.grid()
    pyplot.savefig('DNL.%s'%fmat, dpi=300, format=fmat)
    pyplot.clf()
    pyplot.plot(INL)
    pyplot.xlabel('Input value n')
    pyplot.ylabel('INL(LSB)')
    pyplot.grid()
    pyplot.savefig('INL.%s'%fmat, dpi=300, format=fmat)
    pyplot.clf()
