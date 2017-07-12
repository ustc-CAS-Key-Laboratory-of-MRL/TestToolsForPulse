# coding=UTF-8
# /*************************************************
# Copyright:
# Author:XYJ
# Date:
# Description: 
# **************************************************/
from libs import *
from UseDevs import fpga, tdc, osc

pulse_high = 3.3
vdiv_num = 8


def test(*args, **kwarg):
    pass


def test_hist_ppulse(width=5., gap=100., **kwargs):
    avg = []
    jitter = []
    # todo:
    osc.set_hoffset()
    osc.set_hscale()
    osc.set_voffset()
    osc.set_vscale()
    osc.set_measure()
    osc.set_trigger()

    pulse = []
    fpga.stop()
    osc.clr_sweep()
    pulse.append(['111111111', 0, 0, width])
    pulse.append(['000000000', 0, 0, gap])
    fpga.PBC_type_program(pulse)
    fpga.start(0)
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
        if paras[-1] > 1000:
            avg.append(paras[0])
            jitter.append(paras[1])
            print paras
            break
        time.sleep(1.0)
    hist_data = osc.get_histogram_data()
    write_to_csv(DATAPATH + get_time_str() + 'hist_width_%f.csv' % width, hist_data)


def test_long_time_measure(time_len=86400, width=5., gap=100., type_='width', ch=4, **kwargs):
    """
    :param time_len:
    :param width:
    :param gap:
    :param type_: 'width', 'delay'
    :param ch:
    :param kwargs:
    :return:
    """
    results = [[] for ii in range(ch)]
    # todo: osc
    osc.set_hoffset(-width / 3e9)
    osc.set_hscale(width / 15e9)
    osc.set_voffset(-pulse_high / 2.)
    osc.set_vscale(pulse_high / vdiv_num)
    osc.set_measure(index=1, type_='width', source='C%d' % ch)
    osc.set_trigger(chn=3, threshold=1.5)

    pulse = []
    fpga.stop()
    osc.clr_sweep()
    pulse.append(['111111111', 0, 0, width])
    pulse.append(['000000000', 0, 0, gap])
    fpga.PBC_type_program(pulse)
    start_time = time.clock()
    fpga.start(0)

    time_str = ''
    while time.clock() - start_time < time_len:
        time.sleep(10.)
        for ii in range(ch):
            results[ii].append(osc.get_measure_in_details('P1')['Current'])

        try:
            # save this and delete last
            t = DATAPATH + get_time_str() + 'timelen_%f_%s_%f' % (time_len, type_, width,)
            write_to_csv(t, results)

            if os.path.exists(time_str):
                os.remove(time_str)
            time_str = t
        except:
            traceback.print_exc()


def test_long_time_stability(time_len=86400, delay=5., ch=4, **kwargs):
    """
    :param time_len:
    :param width:
    :param gap:
    :param type_: 'width', 'delay'
    :param ch:
    :param kwargs:
    :return:
    """
    # results = [[] for ii in range(ch)]

    pulse = []
    fpga.stop()

    pulse.append(['111110000', 0, 0, delay])
    pulse.append(['111111111', 0, 0, 100.])
    pulse.append(['000000000', 0, 0, 10000000.])
    fpga.PBC_type_program(pulse)
    start_time = time.clock()
    fpga.start(0)
    # tdc.start()
    dirr = DATAPATH + 'test_long_time_stability_' + get_time_str() + '/'
    os.mkdir(dirr)
    time_str = ''
    index = 0
    while time.clock() - start_time < time_len:
        time.sleep(10.)
        # for ii in range(ch):
        #     results[ii].append(tdc.get_delay())
        tdc.start_and_save(10, dirr + '%d.dat' % index)
        index += 1

        # try:
        #     # save this and delete last
        #     t = DATAPATH + get_time_str() + 'timelen_%f_delay_%f.dat' % (time_len, delay,)
        #     write_to_csv(t, results)
        #
        #     if os.path.exists(time_str):
        #         os.remove(time_str)
        #     time_str = t
        # except:
        #     traceback.print_exc()


def test_std_change_with_delay(delayn_in_10=None, delay_index=9, test_times=5000):
    if delayn_in_10 is None:
        delay = [1., 2., 3., 5.]
        # delay = [1.]
    delays = [0.]
    for i in range(delay_index):
        # for i in [8]:
        for j in range(len(delay)):
            delays.append(delay[j] * 10 ** i)
    # delays = [20, 30, 200, 300, 2000, 3000, 20000, 30000, 200000, 300000, 2000000, 3000000, 20000000, 30000000]
    dirr = DATAPATH + get_time_str() + '/'
    os.mkdir(dirr)

    for delay in delays:
        print 'delay=', delay
        fpga.stop()
        pulse = []
        # pulse.append(['111111010', 0, 0, 10.00])
        # pulse.append(['000000000', 0, 0, delay-10])
        pulse.append(['111110000', 0, 0, delay])
        # pulse.append(['100001111', 0, 0, delay])
        pulse.append(['111111111', 0, 0, 10.000])
        # pulse.append(['100000101', 0, 0, 10.00])
        # pulse.append(['000000000', 0, 0, 1000000.0])
        pulse.append(['000000000', 0, 0, 1000000.0])
        fpga.PBC_type_program(pulse)
        fpga.start(0)
        tdc.start_and_save(test_times, fname=dirr + '%d.txt' % delay)


def test_long_time_delay_change(start=0., step=.05, point=24, ch=0, **kwargs):
    results = [[] for ii in range(ch)]

    for i in range(point):
        pulse = []
        fpga.stop()

        pulse.append(['110000000', 0, 0, start + step * i])
        pulse.append(['111111111', 0, 0, 100.])
        pulse.append(['000000000', 0, 0, 100.])
        fpga.PBC_type_program(pulse)
        start_time = time.clock()
        fpga.start(0)
        result = tdc.start(10000)
        write_to_csv(DATAPATH + get_time_str() + 'ch_%d_delay_change_%f' % (ch, start + step * i,), results)


def test_hist_sequence(time_len=1000., width=100000, seq_loop=100000, **kwargs):
    fpga.stop()
    pulse = []
    for i in xrange(seq_loop * 2):
        # pulse.append(['111111111', 0, 0, width])
        pulse.append(['111110000', 0, 0, width])
        pulse.append(['000000000', 0, 0, width])
        pulse.append(['100001111', 0, 0, width])
        pulse.append(['000000000', 0, 0, width])

    print 'pulse=', len(pulse)
    fpga.PBC_type_program(pulse)
    # start_time = time.clock()
    fpga.start(1)

    tdc.start_and_save(seq_loop,
                       DATAPATH + get_time_str() + 'test_hist_sequence_width_%e_loop_%d.csv' % (width, seq_loop))
    # while time.clock() - start_time < time_len:
    #     time.sleep(10.)
    #     tdc.start()


if __name__ == '__main__':
    # test_hist_sequence()
    test_std_change_with_delay()
    # for delay in [10., 1000, 1000000, 1000000000]:
    #     test_long_time_stability(delay=delay)
