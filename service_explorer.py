import argparse
import asyncio

from bleak import BleakClient


def parse_arg():
    parser = argparse.ArgumentParser(description="Test notification of the specified device.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


async def run(address):
    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        for service in client.services:
            print("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                print(
                    "\t[Characteristic] {0}: (Handle: {1}) ({2}) | Name: {3}, Value: {4} ".format(
                        char.uuid,
                        char.handle,
                        ",".join(char.properties),
                        char.description,
                        value,
                    )
                )
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    print(
                        "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                            descriptor.uuid, descriptor.handle, bytes(value)
                        )
                    )


if __name__ == "__main__":
    args = parse_arg()
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(args.ADDRESS))
