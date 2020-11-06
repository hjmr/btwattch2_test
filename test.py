import argparse
import asyncio

from bleak import BleakClient

SVC_TX_POWER = ("00001804-0000-1000-8000-00805f9b34fb")
CHAR_TX_POWER = ("00002a07-0000-1000-8000-00805f9b34fb")


def parse_arg():
    parser = argparse.ArgumentParser(description="List services of the specified device.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


async def run(address, svc_uuid, char_uuid):
    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        svc = await get_service(client, svc_uuid)
        char_tx_power = await get_characteristic(svc, char_uuid)

        value = await client.read_gatt_char(char_tx_power)
        print("Data: {} {}".format(int(value), value))


async def get_service(client, svc_uuid):
    svcs = await client.get_services()
    return svcs.get_service(svc_uuid)


async def get_characteristic(service, char_uuid):
    return service.get_characteristic(char_uuid)


args = parse_arg()
loop = asyncio.get_event_loop()
loop.run_until_complete(run(args.ADDRESS, SVC_TX_POWER, CHAR_TX_POWER))
