from abc import ABC, abstractmethod
import numpy as np
input_str = '9C0141080250320F1802104A08'
with open('input', 'r') as f:
    input_str = f.read()

input_str = input_str.strip()
print(input_str)


class Packet(ABC):

    def __init__(self, type_id, version):
        self.type = type_id
        self.version = version
        self.is_literal = self.type == 4

    def get_type(self):
        return 'Literal' if self.is_literal else 'Operator'

    def decode_header(self, stream):
        version = int(stream[:3], 2)
        type_id = int(stream[3:6], 2)
        return version, type_id, stream[6:]

    @abstractmethod
    def version_sum(self):
        pass

    @abstractmethod
    def decode(self, stream):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_value(self):
        pass


class LiteralPacket(Packet):
    def __init__(self, type_id, version):
        super().__init__(type_id, version)
        self.value = None

    def decode(self, stream):
        out = ''
        last_chunk = 1
        while last_chunk != 0:
            last_chunk = int(stream[0])
            out += stream[1:5]
            stream = stream[5:]
        self.value = int(out, 2)
        return self.value, stream

    def version_sum(self):
        return self.version

    def get_value(self):
        return self.value

    def __str__(self):
        out = f'{self.get_type()} (ver {self.version}): [value: {self.value}]'
        return out

    def __repr__(self):
        return self.__str__()


class OperatorPacket(Packet):
    def __init__(self, type_id, version):
        super().__init__(type_id, version)
        self.subpackets = []

    def decode_payload(self, stream):
        version, type_id, stream = self.decode_header(stream)
        if type_id == 4:
            packet = LiteralPacket(type_id, version)
            _, stream = packet.decode(stream)
            self.subpackets.append(packet)
        else:
            packet = OperatorPacket(type_id, version)
            _, stream = packet.decode(stream)
            self.subpackets.append(packet)
        return stream

    def decode(self, stream):
        length_type = int(stream[0])
        length_type = 11 if length_type == 1 else 15
        length = int(stream[1:length_type+1], 2)
        stream = stream[length_type+1:]
        if length_type == 15:
            payload = stream[:length]
            while payload:
                payload = self.decode_payload(payload)
            stream = stream[length:]
        else:
            for i in range(length):
                stream = self.decode_payload(stream)
        return self, stream

    def version_sum(self):
        return self.version + sum([x.version_sum() for x in self.subpackets])

    def get_value(self):
        if self.type == 0:  # sum
            return np.sum([x.get_value() for x in self.subpackets])
        elif self.type == 1:  # product
            return np.product([x.get_value() for x in self.subpackets])
        elif self.type == 2:  # min
            return np.min([x.get_value() for x in self.subpackets])
        elif self.type == 3:  # max
            return np.max([x.get_value() for x in self.subpackets])
        elif self.type == 5:  # less than
            assert len(self.subpackets) == 2, 'Too many subpackets for >!'
            return int(self.subpackets[0].get_value() >
                       self.subpackets[1].get_value())
        elif self.type == 6:  # greater than
            assert len(self.subpackets) == 2, 'Too many subpackets for <!'
            return int(self.subpackets[0].get_value() <
                       self.subpackets[1].get_value())
        elif self.type == 7:  # equals
            assert len(self.subpackets) == 2, 'Too many subpackets for ==!'
            return int(self.subpackets[0].get_value() ==
                       self.subpackets[1].get_value())
        else:
            raise NotImplementedError(f'{self.type} is not a valid operator!')

    def __str__(self):
        out = (
            f'{self.get_type()} (ver {self.version}): ' +
            f'[subpackets: {[str(x) for x in self.subpackets]}]')
        return out

    def __repr__(self) -> str:
        return self.__str__()


def decode_header(stream):
    version = int(stream[:3], 2)
    type_id = int(stream[3:6], 2)
    return version, type_id, stream[6:]


def decode_packet(input_str):
    stream = ''.join([format(int(x, 16), '04b') for x in input_str])
    version, type_id, stream = decode_header(stream)
    if type_id == 4:
        packet = LiteralPacket(type_id, version)
        _, stream = packet.decode(stream)
        return packet, stream
    else:
        packet = OperatorPacket(type_id, version)
        _, stream = packet.decode(stream)
        return packet, stream


packet, stream = decode_packet(input_str)
# something goes wrong here
# print(packet)
# print(stream)
print(f'Version sum: {packet.version_sum()}')
print(f'Stream value: {packet.get_value()}')
