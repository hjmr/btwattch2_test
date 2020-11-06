from abc import ABC
from abc import abstractmethod

CMD_HEADER = 0xAA


class DataHandler(ABC):
    def __init__(self):
        super(DataHandler, self).__init__()
        self.data_length = 0
        self.data_buffer = bytearray()

    def new_data(self, data):
        for idx in range(len(data)):
            if data[idx] == CMD_HEADER:
                self.data_buffer.clear()
                self.data_length = int.from_bytes(data[idx+1:idx+3], byteorder='big')
                idx += 3
            else:
                self.data_buffer.append(data[idx])

            if 0 < self.data_length and self.data_length <= len(self.data_buffer):
                self.process_data(self.data_buffer)
                self.data_buffer.clear()
                self.data_length = 0

    @abstractmethod
    def process_data(self, data):
        pass
