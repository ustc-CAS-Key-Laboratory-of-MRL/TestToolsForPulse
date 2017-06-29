# coding=UTF-8
# /*************************************************
# Copyright:
# Author:XYJ
# Date:
# Description: 
# **************************************************/
from libs import *
from UseDevs import fpga, tdc, osc


# import LecroyInterface as osc

def test(*args, **kwarg):
    pass


pulse_high = 3.3
vdiv_num = 8


def pulse_step_test(start=5., step=.05, point=24, gap=20.):
    avg = []
    jitter = []

    osc.set_measure()
    osc.set_trigger()
    for i in range(point):
        width = start + step * i
        osc.set_hoffset(-width / 3e9)
        osc.set_hscale(width / 15e9)
        osc.set_voffset(-pulse_high / 2.)
        osc.set_vscale(pulse_high / vdiv_num)

        pulse = []
        fpga.stop()
        osc.clr_sweep()
        pulse.append(['111111111', 0, 0, width])
        pulse.append(['000000000', 0, 0, gap])
        fpga.PBC_type_program(pulse)
        fpga.start()
        time.sleep(10.0)
        while True:
            sdata = osc.get_measure('P1')
            sdata = sdata.split(',')
            paras = []
            # must in order
            get = ['AVG', 'SIGMA', 'SWEEPS']
            for j in range(len(sdata)):
                if sdata[j] in get:
                    try:
                        paras.append(float(sdata[j + 1]))
                    except:
                        paras = []
                        break
            if len(paras) == 0:
                continue
            if paras[-1] > 10000:
                avg.append(paras[0])
                jitter.append(paras[1])
                print paras
                break
            time.sleep(1.0)
    ideals = [start + ii * step for ii in range(point)]
    data = np.array([ideals, avg, jitter])
    write_to_csv(DATAPATH + get_time_str() + 'start_%f_step_%f_point_%d.csv' % (start, step, point), data)


def pulse_step_tdc_test(start=10., step=.05, point=24, gap=1000000., test_times=10000, channel='00000011'):
    dirr = DATAPATH + 'pulse_step_tdc_test_%s_' % channel + get_time_str() + '/'
    os.mkdir(dirr)
    ch2_on = '1' + channel.replace('1', '0', 1)
    i = len(channel) - 1
    while i > 0 and channel[i] == '0': i -= 1
    ch1_on = '1' + channel[:i] + '0' + channel[i + 1:]
    print ch1_on, ch2_on
    for i in range(point):
        pulse = []
        fpga.stop()
        pulse.append([ch1_on, 0, 0, step * i])
        pulse.append(['1'+channel, 0, 0, start])
        pulse.append(['000000000', 0, 0, gap])
        fpga.PBC_type_program(pulse)
        fpga.start(0)
        tdc.start_and_save(test_times, fname=dirr + '_ch_1_%s.dat' % channel)

    for i in range(point):
        pulse = []
        fpga.stop()
        pulse.append([ch2_on, 0, 0, step * i])
        pulse.append(['1'+channel, 0, 0, start])
        pulse.append(['000000000', 0, 0, gap])
        fpga.PBC_type_program(pulse)
        fpga.start(0)
        tdc.start_and_save(test_times, fname=dirr + '_ch_2_%s.dat' % channel)


if __name__ == '__main__':
    # for i in ['00010010', '11000000', '00000011']:
    #     pulse_step_tdc_test(channel=i)
    pulse_step_tdc_test(channel='10001000')
    raw_input('please channe sma connector')
    pulse_step_tdc_test(channel='01000100')
    raw_input('please channe sma connector')
    pulse_step_tdc_test(channel='00100010')
    raw_input('please channe sma connector')
    pulse_step_tdc_test(channel='00010001')