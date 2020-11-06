import argparse
import asyncio

from utils import decode_data

from bleak import BleakClient

CMD_HEADER = 0xaa

CHAR_UART_RX = ("6e400002-b5a3-f393-e0a9-e50e24dcca9e")
CHAR_UART_NOTIFY = ("6e400003-b5a3-f393-e0a9-e50e24dcca9e")


def parse_arg():
    parser = argparse.ArgumentParser(description="Test reading watt data.")
    parser.add_argument("ADDRESS", type=str, help="A device address.")
    return parser.parse_args()


data_length = 0
data_buffer = []


def process_data(data):
    for idx, x in enumerate(data):
        if x == CMD_HEADER:
            data_buffer.clear()
            data_length = int.from_bytes(data[idx+1:idx+2], byteorder='big') + 3  # 3 for header
        data_buffer.append(x)
        if 0 < data_length and len(data_buffer) == data_length:
            ret = decode_data(data_buffer)
            print(ret)
            data_buffer.clear()


def notification_handler(sender, data):
    process_data(data)


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
