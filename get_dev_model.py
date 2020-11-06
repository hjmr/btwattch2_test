import argparse
import asyncio

from bleak import BleakClient

MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"


def parse_arg():
    parser = argparse.ArgumentParser(description="Get model number of the specified device.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


async def run(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

args = parse_arg()
loop = asyncio.get_event_loop()
loop.run_until_complete(run(args.ADDRESS))
