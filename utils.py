from datetime import datetime


def decode_data(buffer):
    field_lengths = (
        ('header', 1),  # 0
        ('length', 2),  # 1, 2
        ('command', 1),  # 3
        ('error_code', 1),  # 4
        ('current', 3),  # 5, 6, 7
        ('voltage', 3),  # 8, 9, 10
        ('power', 3),  # 11, 12, 13
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
        v = int.from_bytes(buffer[i:i+l], byteorder='big')
        d[k] = v
        i += l

    ret = {}
    # ret['datetime'] = datetime(2000 + d['year'], d['month'], d['day'], d['hour'],
    #                           d['minute'], d['second']).strftime('%Y-%m-%d %H:%M:%S')
    ret['V'] = d['voltage'] / 1000.0
    ret['mA'] = d['current'] / 128.0
    ret['W'] = d['power'] * 5.0 / 1000.0

    return d
