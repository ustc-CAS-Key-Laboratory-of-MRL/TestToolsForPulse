# coding=UTF-8
# /*************************************************
# Copyright:
# Author:XYJ
# Date:
# Description: 
# **************************************************/
import interface.DAQs.Lecroy735 as OSC
import interface.DDR3_USB_8chn_Continue_counter_V1 as ASG
import interface.TDC as TDC
import interface.Gen as Gen
import os
import sys

for pp in sys.path:
    if 'Pulse' in pp:
        os.chdir(pp)
        break

osc = OSC.Digitizer()
global fpga
fpga = ASG.FPGADev(dev_index=1)
tdc = TDC.FPGA(dev_index=0)


def calibrate():
    pulse = []
    for i in range(1):
        pulse.append(['111111111', 0, 0, 501.])
        # pulse.append(['001000000', 0, 0, 80.000 + i * 0.05])
        pulse.append(['000000000', 0, 0, 1000993.5])
    fpga.PBC_type_program(pulse)
    fpga.start(0)
    tdc.start_and_save(3000000, 'calibrate.dat')


if __name__ == '__main__':
    calibrate()
