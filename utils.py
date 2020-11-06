from datetime import datetime

import crcmod


def crc8(data):
    crc8_func = crcmod.mkCrcFun(0x185, initCrc=0, rev=False)
    return crc8_func(data).to_bytes(1, 'big')


def decode_data(buffer):
    field_lengths = (
        ('header', 1),  # 0
        ('length', 2),  # 1, 2
        ('command', 1),  # 3
        ('error_code', 1),  # 4
        ('current', 6),  # 5, 6, 7
        ('voltage', 6),  # 8, 9, 10
        ('power', 6),  # 11, 12, 13
        ('second', 1),  # 14
        ('minute', 1),  # 15
        ('hour', 1),  # 16
        ('day', 1),  # 17
        ('month', 1),  # 18
        ('year', 1)  # 19
    )
    d = {}
    i = 0
    for k, l in field_lengths:
        v = int.from_bytes(buffer[i:i+l], byteorder='little')
        d[k] = v
        i += l

    ret = {}
    # ret['datetime'] = datetime(2000 + d['year'], d['month'], d['day'], d['hour'],
    #                           d['minute'], d['second']).strftime('%Y-%m-%d %H:%M:%S')
    ret['V'] = d['voltage'] / 1000.0
    ret['mA'] = d['current'] / 128.0
    ret['W'] = d['power'] * 5.0 / 1000.0

    return d


def encode_datetime(year, month, day, hour, minute, second):
    return bytearray([second, minute, hour, day, month-1, year-1900])


if __name__ == "__main__":
    command = bytearray([0xaa, 0x00, 0x08, 0x01])
    encoded_dt = encode_datetime(2020, 9, 26, 1, 35, 00)
    cmd = command + encoded_dt + bytes([5])
    cmd += crc8(cmd)
    data_str = ' '.join(format(x, '02x') for x in cmd)
    print(data_str)
