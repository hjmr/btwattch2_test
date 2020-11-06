import argparse
import asyncio

from bleak import BleakClient


CHAR_TX_POWER = ("00002a07-0000-1000-8000-00805f9b34fb")


def parse_arg():
    parser = argparse.ArgumentParser(description="Test notification of the specified device.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


async def run(address):
    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        value = await client.read_gatt_char(CHAR_TX_POWER)
        print("Data: {} ({}:{})".format(int(value[0]), value, type(value)))


if __name__ == "__main__":
    args = parse_arg()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.ADDRESS))
