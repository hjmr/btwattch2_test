import argparse
import asyncio

from bleak import BleakClient


def parse_arg():
    parser = argparse.ArgumentParser(description="List services of the specified device.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


async def print_services(address):
    async with BleakClient(address) as client:
        svcs = await client.get_services()
        for s in svcs:
            print("Service: {} {}".format(s.uuid, s.description))


args = parse_arg()
loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(args.ADDRESS))
