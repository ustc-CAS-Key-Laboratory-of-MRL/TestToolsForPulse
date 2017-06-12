# coding=UTF-8
# /*************************************************
# Copyright:
# Author:XYJ
# Date:
# Description: 
# **************************************************/
from libs import *
from FPGA import fpga
from OSC import osc


# import LecroyInterface as osc

def test(*args, **kwarg):
    pass


# osc = osc.Digitizer()
# osc.open()

def pulse_step_test(start=5., step=.05, point=24, gap=20.):
    avg = []
    jitter = []
    # todo:
    osc.set_hoffset()
    osc.set_hscale()
    osc.set_voffset()
    osc.set_vscale()
    osc.set_measure()
    osc.set_trigger()
    for i in range(point):
        pulse = []
        fpga.stop()
        osc.clr_sweep()
        pulse.append(['111111111', 0, 0, start + step * i])
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
            if paras[-1] > 1000:
                avg.append(paras[0])
                jitter.append(paras[1])
                print paras
                break
            time.sleep(1.0)
    ideals = [start + ii * step for ii in range(point)]
    data = np.array([ideals, avg, jitter])
    write_to_csv(DATAPATH + get_time_str() + 'start_%f_step_%f_point_%d.csv'%(start, step, point), data)


if __name__ == '__main__':
    pass
