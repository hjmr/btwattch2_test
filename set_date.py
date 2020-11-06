import argparse
import asyncio
from datetime import datetime

from utils import encode_datetime, crc8

from bleak import BleakClient


CHAR_UART_RX = ("6e400002-b5a3-f393-e0a9-e50e24dcca9e")
CHAR_UART_NOTIFY = ("6e400003-b5a3-f393-e0a9-e50e24dcca9e")


def parse_arg():
    parser = argparse.ArgumentParser(description="Test notification of the specified device.")
    parser.add_argument("--datetime", type=str, help="Specify date and time in %Y-%m-%d %H:%M:%S format.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    data_str = ' '.join(format(x, '02x') for x in data)
    print("[Notification] {0}: {1}".format(sender, data_str))


async def run(address, dt=None):

    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        if dt is None:
            dt = datetime.now()

        set_date_command = bytearray([0xaa, 0x00, 0x08])
        start_data = bytes([0x01])
        end_data = bytes([0x05])

        encoded_now = encode_datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        data_body = start_data + encoded_now + end_data
        write_data = set_date_command + data_body + crc8(data_body)

        await client.start_notify(CHAR_UART_NOTIFY, notification_handler)

        await client.write_gatt_char(CHAR_UART_RX, write_data)
        await asyncio.sleep(5.0)

        await client.stop_notify(CHAR_UART_NOTIFY)


if __name__ == "__main__":
    args = parse_arg()
    dt = None
    if args.datetime is not None:
        dt = datetime.strptime(args.datetime, '%Y-%m-%d %H:%M:%S')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.ADDRESS, dt))
