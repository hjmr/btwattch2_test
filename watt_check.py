import argparse
import asyncio
import time

from utils import decode_watt_data
from data_handler import DataHandler

from bleak import BleakClient


CHAR_UART_RX = ("6e400002-b5a3-f393-e0a9-e50e24dcca9e")
CHAR_UART_NOTIFY = ("6e400003-b5a3-f393-e0a9-e50e24dcca9e")


class WattDataHandler(DataHandler):
    def _process_data(self, data):
        ret = decode_watt_data(data)
        print(ret)


watt_handler = WattDataHandler()


def parse_arg():
    parser = argparse.ArgumentParser(description="Test reading watt data.")
    parser.add_argument("-d", "--duration", type=float, default=5.0, help="A duration in sec. to check watt.")
    parser.add_argument("-i", "--interval", type=float, default=1.0, help="An interval in sec. to check watt.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


def notification_handler(sender, data):
    watt_handler.new_data(data)


async def run(address, duration, interval):
    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        write_value = bytearray([0xaa, 0x00, 0x01, 0x08, 0xb3])
        await client.start_notify(CHAR_UART_NOTIFY, notification_handler)

        start_time = time.time()
        while time.time() - start_time < duration:
            await asyncio.sleep(interval)
            await client.write_gatt_char(CHAR_UART_RX, write_value)

        await client.stop_notify(CHAR_UART_NOTIFY)


if __name__ == "__main__":
    args = parse_arg()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.ADDRESS, args.duration, args.interval))
