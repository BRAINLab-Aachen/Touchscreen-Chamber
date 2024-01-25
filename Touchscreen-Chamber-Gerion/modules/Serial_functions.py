import serial
from time import time, sleep
from serial.tools import list_ports


MODULE_INFO = 255  # returns module information


def search_for_microcontroller_by_name(name):
    ports_found = list_ports.comports()
    for port in ports_found:
        try:
            serial_obj = open_serial(port.device, baudrate=9600)
            name_returned = read_module_name(serial_obj)

            if name == name_returned:
                return serial_obj
            else:
                serial_obj.close()
            #
        except Exception as e:
            print(e)
            print(port)
            pass
        #
    #

    raise Exception(name + ' Microcontroller NOT FOUND!')
#


def read_module_name(serial_obj):
    serial_obj.read_all()  # flush Serial

    # Ask the COM device to identify itself
    _send_byte_alone(serial_obj=serial_obj, header_byte=MODULE_INFO)
    sleep(0.05)

    # Ignore the first 5, they are part of the protocol but not relevant here
    _ = serial_obj.read(size=5)

    # read name length
    name_length = int.from_bytes(serial_obj.read(size=1), byteorder='big')

    # read name
    name = serial_obj.read(size=name_length)

    # read last 0 byte
    serial_obj.read(size=1)

    return name.decode()
#


def open_serial(COM_port='COM3', baudrate=9600):
    serial_obj = serial.Serial(COM_port, baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)
    # try to close previous connection in case there was an error.
    try:
        serial_obj.close()
    except:
        pass
    #
    serial_obj.open()

    return serial_obj
#


def _send_byte_alone(serial_obj, header_byte):
    serial_obj.write(bytes(chr(header_byte), 'ascii'))
#


def _send_dec_values(serial_obj, header_byte, values):
    # IMPORTANT!!!
    # before I was sending each byte individually for simplicity.
    # PROBLEM: If not read by the teensy it stops transmitting after 12 bytes.
    # 1. It turns out, that the USB-Serial sends Packages of 64byte.
    # 2. However, the teensy rx-buffer only holds 12 packages
    # SOLUTION: I'm converting my input into a long bytearray and send that.
    # Possible issues: If the message becomes > 64byte it might cause issues, or not.
    # The message might just be split into 2 packages. We'll see.

    char_list = [list(str(value)) for value in values]
    value_lengths = [len(value) for value in char_list]

    temp_str = ''
    for element in char_list:
        for c in element:
            temp_str += c
        #
    #
    serial_obj.write(bytes(chr(header_byte), 'ascii') + bytearray(value_lengths) + temp_str.encode())
#


def send_data_until_confirmation(serial_obj, header_byte, data=None):
    # header_byte:
    # START_TRIAL = 70

    while True:
        serial_obj.read_all()  # flush Serial

        # Start Trial
        if data is None:
            _send_byte_alone(serial_obj, header_byte)
        else:
            _send_dec_values(serial_obj, header_byte, data)
        #
        st = time()

        received = False
        while time() - st < 0.2:
            # input_byte = s.readline().decode().rstrip()
            if serial_obj.in_waiting:
                # input_byte = serial_obj.read().decode().rstrip()
                input_byte = int.from_bytes(serial_obj.read(size=1), byteorder='big')

                if input_byte == 14:
                    # got byte
                    # print('GOT BYTE')
                    serial_obj.read_all()  # flush Serial
                    received = True
                    break
                #

                if input_byte == 15:
                    # resend
                    # print('DID ABORT')
                    serial_obj.read_all()  # flush Serial
                    break
                #
            #
        #

        if received:
            # successful
            break
        #
    #
#


def wait_for_signal_byte(serial_obj, target_bytes, timeout=0):
    # timeout = 0: don't wait, just check if the Byte is there or not and return
    active_timeout = timeout >= 0
    received = False
    input_byte = -1
    st = time()
    while True:
        # serial_obj.read_until(bytes(target_chr, 'ascii'), size=1)
        # input_byte = s.readline().decode().rstrip()
        if serial_obj.in_waiting:
            input_byte = int.from_bytes(serial_obj.read(size=1), byteorder='big')
            try:
                if input_byte in target_bytes:
                    received = True

                    serial_obj.write(bytes(chr(14), 'ascii'))
                    # print('Send: GOT_BYTE')
                    # serial_obj.read_all()  # flush Serial

                    break
                else:
                    # print("Unexpected Byte: %d, %f" % (input_byte, time() - t))
                    # serial_obj.write(bytes(chr(14), 'ascii'))
                    serial_obj.read_all()  # flush Serial
                #
            except Exception as e:
                print(e)
            #
        #

        if active_timeout:
            if time() - st >= timeout:
                break
            #
        #
    #

    return input_byte, received
#
