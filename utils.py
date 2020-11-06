from datetime import datetime

import crcmod


def crc8(data):
    crc8_func = crcmod.mkCrcFun(0x185, initCrc=0, rev=False)
    return crc8_func(data).to_bytes(1, 'big')


def decode_watt_data(buffer):
    field_lengths = (
        # ('header', 1),
        # ('length', 2),
        ('command', 1),
        ('error_code', 1),
        ('voltage', 6),
        ('current', 6),
        ('power', 6),
        ('second', 1),
        ('minute', 1),
        ('hour', 1),
        ('day', 1),
        ('month', 1),
        ('year', 1)
    )
    d = {}
    i = 0
    for k, l in field_lengths:
        v = int.from_bytes(buffer[i:i+l], byteorder='little')
        d[k] = v
        i += l

    ret = {}
    ret['datetime'] = datetime(1900+d['year'], d['month']+1, d['day']+1,
                               d['hour'], d['minute'], d['second']).strftime('%Y-%m-%d %H:%M:%S')
    ret['V'] = d['voltage'] / 16 ** 6
    ret['mA'] = d['current'] / 32 ** 6
    ret['W'] = d['power'] / 16 ** 6

    return ret


def encode_datetime(year, month, day, hour, minute, second):
    return bytearray([second, minute, hour, day-1, month-1, year-1900])


if __name__ == "__main__":
    command = bytearray([0xaa, 0x00, 0x08])
    encoded_dt = bytes([1]) + encode_datetime(2020, 9, 27, 1, 35, 00) + bytes([5])
    cmd = command + encoded_dt
    cmd += crc8(encoded_dt)
    data_str = ' '.join(format(x, '02x') for x in cmd)
    print(data_str)
