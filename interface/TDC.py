import ctypes
import time


def num_to_bytes(num, bytenum):
    bytes_ = ''
    while num > 255:
        bytes_ = chr(num % 256) + bytes_
        num /= 256
    bytes_ = chr(num % 256) + bytes_
    if len(bytes_) < bytenum:
        bytes_ = (bytenum - len(bytes_)) * '\x00' + bytes_
    else:
        bytes_ = bytes_[len(bytes_) - bytenum:]
    return bytes_


class FPGA():
    def __init__(self, dev_index=1, test_mode=False):
        if test_mode:
            import random

            def read():
                return random.choice(
                    ['\xff\x00\x00\x00', '\xff\x00\x00\x01', '\x00' * 4, '\x11' * 4, '\x22' * 4, '\x11' * 6,
                     '\xff' * 4])

            def write(msg):
                return len(msg)

            class dll:
                def flushInputBuffer(self):
                    pass

            self.read = read
            self.write = write
            self.dll = dll()
            self.stop()
            return
        import platform
        bits = platform.architecture()[0]
        dll_load = False
        try:
            self.dll = ctypes.cdll.LoadLibrary('xyj.dll')
            dll_load = True
        except:
            print 'Load xyj.dll fail!'
        try:
            if not dll_load:
                if '32bit' in bits:
                    self.dll = ctypes.cdll.LoadLibrary('xyj_x86.dll')
                else:
                    self.dll = ctypes.cdll.LoadLibrary('xyj_x64.dll')
        except:
            import traceback
            traceback.print_exc()
            print '\nLoad FPGA USB fail!\n'
            return
        self.open(dev_index)

        self.dll.read.restype = ctypes.c_bool
        self.dll.read_until.restype = ctypes.c_bool
        self.dll.GetPara.restype = ctypes.c_ulong
        self.stop()

    def open(self, index=0):
        self.dll.open.restype = ctypes.c_bool
        return self.dll.open(ctypes.c_byte(index))

    def stop(self):
        """
        stop the device.
        :return:
        """
        # use for stop counter
        self.run_flag = False
        time.sleep(0.01)
        self.write('\x00' * 2)
        time.sleep(0.01)
        # clear buffer
        self.dll.flushInputBuffer()
        global CountDataBuf
        CountDataBuf = [0, []]

    def read(self, num=4096):
        bufp = (ctypes.c_ubyte * 4100)()
        # bufp = ctypes.c_char_p('\x00' * num)
        cnum = ctypes.c_long(num)
        cnum_p = ctypes.pointer(cnum)

        if not self.dll.read(bufp, cnum_p):
            # fh.write('F%d\n' % cnum_p.contents.value)
            self.dll.ResetInputEnpt()
            return ''
        # fh.write('S%d\n' % cnum_p.contents.value)
        # fh.flush()
        # print num, 'rx num', cnum_p.contents.value
        return str(bytearray(bufp))[:cnum_p.contents.value]

    def write(self, msg):
        bufp = ctypes.c_char_p(msg)
        self.dll.write(bufp, ctypes.c_long(len(msg)))
        return len(msg)

    def file_start(self, period, read_num1):
        self.dll.flushInputBuffer()
        self.start(read_num1)
        self.datasave(read_num1, period)

    def start(self, cnt_num):
        """
        play waveform in all channel
        """
        # todo:don't play all channels all the time
        # self.write('\x00\x65')
        # time.sleep(2)
        print('start')
        cnt_data = '\x00\x01' + num_to_bytes(cnt_num, 4)
        # cnt_data='\x00\x00'
        # cnt_data='\x02\x09'+'\x00\x01'+ num_to_bytes(cnt_num, 4)
        self.write(cnt_data)

    def datasave(self, cnt_num, period_time=0):
        print('save')

        file_num = 'tdc_20ch_8ns_crs_b1_bit_data_retest_125M_balance_0m.csv'
        # file_num='tdc_20ch_4ns_crs_b1_bit_data_retest_500M_balance_code.csv'   
        # file_num='tdc_20ch_4ns_crs_b1_bit_71_data_'+'%d' %period_time + 'ns.csv'

        # print(period_str)

        f = file(file_num, 'wb')
        # ff=file(file_num1 ,'wb')
        cnt = 0
        data = ''
        while cnt < cnt_num * 280:
            data = self.read()
            if data != '':
                cnt += len(data)
                print('%d\n' % len(data))
                print('%d\n' % cnt)
                # f.write(data)
                for i in range(len(data)):
                    f.write(data[i])
                    # a=ord(data[i])
                    # f.write('%02x'%a)
            else:
                continue
        f.flush()
        f.close()
        # ff.flush()
        # ff.close()


if __name__ == '__main__':
    fpga = FPGA(0)

    fpga.dll.flushInputBuffer()
    read_num = 100000
    # fpga.file_start(0,read_num)
    fpga.start(read_num)
    fpga.datasave(read_num)
