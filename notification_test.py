import argparse
import asyncio

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

        write_value = bytearray([0xaa, 0x00, 0x01, 0x08, 0xb3])
        await client.write_gatt_char(CHAR_UART_RX, write_value)
        await asyncio.sleep(5.0)

        await client.stop_notify(CHAR_UART_NOTIFY)


if __name__ == "__main__":
    args = parse_arg()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.ADDRESS))
