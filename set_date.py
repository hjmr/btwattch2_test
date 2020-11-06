import argparse
import asyncio
from datetime import datetime

from utils import encode_datetime

from bleak import BleakClient


CHAR_UART_RX = ("6e400002-b5a3-f393-e0a9-e50e24dcca9e")
CHAR_UART_NOTIFY = ("6e400003-b5a3-f393-e0a9-e50e24dcca9e")


def parse_arg():
    parser = argparse.ArgumentParser(description="Test notification of the specified device.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    data_str = ' '.join(format(x, '02x') for x in data)
    print("[Notification] {0}: {1}".format(sender, data_str))


async def run(address):

    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        await client.start_notify(CHAR_UART_NOTIFY, notification_handler)

        set_date_command = bytearray([0xaa, 0x00, 0x08, 0x01])

        dt_now = datetime.now()
        encoded_now = encode_datetime(dt_now.year, dt_now.month, dt_now.day, dt_now.hour, dt_now.minute, dt_now.second)

        # write_data = set_date_command + encoded_now
        write_data = bytearray([0xaa, 0x00, 0x08, 0x01, 0x00, 0x23, 0x01, 0x1a, 0x08, 0x78, 0x05, 0x2f])

        await client.write_gatt_char(CHAR_UART_RX, write_data)
        await asyncio.sleep(5.0)

        await client.stop_notify(CHAR_UART_NOTIFY)


if __name__ == "__main__":
    args = parse_arg()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.ADDRESS))
