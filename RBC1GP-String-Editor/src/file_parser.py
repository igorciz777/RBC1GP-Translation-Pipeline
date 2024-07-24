import struct

class RivalData:
    def __init__(self, data):
        unpacked_data = struct.unpack('<3s I I B B 11s B 507s 24s 84s 26s 34s 232s 132s 48s 48s 48s 48s 48s 48s 24s 24s', data)
        self.idx = unpacked_data[0]
        self.something = unpacked_data[1]
        self.something2 = unpacked_data[2]
        self.zero1 = unpacked_data[3]
        self.weirdCarValue = unpacked_data[4]
        self.zero2 = unpacked_data[5]
        self.carBodyId = unpacked_data[6]
        self.unknown = unpacked_data[7]
        self.nickname = unpacked_data[8]
        self.unknown2 = unpacked_data[9]
        self.name = unpacked_data[10]
        self.job = unpacked_data[11]
        self.bio1 = unpacked_data[12]
        self.dialog1 = unpacked_data[13]
        self.dialog2 = unpacked_data[14]
        self.dialog3 = unpacked_data[15]
        self.dialog4 = unpacked_data[16]
        self.dialog5 = unpacked_data[17]
        self.dialog6 = unpacked_data[18]
        self.dialog7 = unpacked_data[19]
        self.dialogShort1 = unpacked_data[20]
        self.dialogShort2 = unpacked_data[21]

def read_file(file_name):
    with open(file_name, 'rb') as f:
        data = f.read()
    return data

def write_file(file_name, data):
    with open(file_name, 'wb') as f:
        f.write(data)

def read_string_locations(data, endian='<'):
    string_locations = []
    first_start_offset = struct.unpack(endian + 'I', data[0:4])[0]
    first_end_offset = struct.unpack(endian + 'I', data[4:8])[0]
    current_file_offset = 4
    string_locations.append((first_start_offset, first_end_offset))
    while current_file_offset < first_start_offset:
        start_offset = struct.unpack(endian + 'I', data[current_file_offset:current_file_offset+4])[0]
        try:
            end_offset = struct.unpack(endian + 'I', data[current_file_offset+4:current_file_offset+8])[0]
        except struct.error:
            end_offset = len(data)
        string_locations.append((start_offset, end_offset))
        current_file_offset += 4
    return string_locations

def find_strings_with_terminator(data, terminator=b'\xff\xff'):
    locations = []
    current_offset = 0
    while current_offset < len(data):
        next_offset = data.find(terminator, current_offset)
        if next_offset == -1:
            break
        locations.append((current_offset, next_offset + len(terminator)))
        current_offset = next_offset + len(terminator)
    return locations

def load_encoding_table(tbl_file_name):
    encoding_table = {}
    decoding_table = {}
    with open(tbl_file_name, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith("#") or line.startswith("//"):
                continue
            line = line.strip()
            if '=' in line:
                hex_value, char = line.split('=')
                hex_value = hex_value.strip()
                char = char.strip()
                try:
                    encoding_table[bytes.fromhex(hex_value)] = char
                    decoding_table[char] = bytes.fromhex(hex_value)
                except ValueError:
                    print(f"Skipping invalid line: {line}")
    return encoding_table, decoding_table

def decode_string(data, encoding_table):
    decoded_string = ""
    i = 0
    while i < len(data):
        matched = False
        for hex_value, char in encoding_table.items():
            if data[i:i + len(hex_value)] == hex_value:
                if char == "ASCII_SPACE":
                    char = " "
                if char == "EUCJP_SPACE":
                    char = "　"
                if char == "COLOR_START#":
                    color = data[i+4:i+8].hex().upper()
                    char = f"#{color}"
                    i += 4
                decoded_string += char
                i += len(hex_value)
                matched = True
                break
        if not matched:
            decoded_string += data[i:i + 1].decode('ascii', errors='ignore')
            i += 1
    return decoded_string

def read_strings(data, string_locations, encoding_table, use_terminator=False):
    strings = []
    for start, end in string_locations:
            raw_string = data[start:end]
            string = decode_string(raw_string, encoding_table)
            strings.append(string)
    return strings

def encode_string(input_string, decoding_table):
    encoded_bytes = b""
    for char in input_string:
        if char == " ":
            char = "ASCII_SPACE"
        if char == "　":
            char = "EUCJP_SPACE"
        if char in decoding_table:
            encoded_bytes += decoding_table[char]
        else:
            continue
    return encoded_bytes.hex()

def realign_offsets(string_locations, data, encoding_table, strings):
    new_data = b""
    new_offsets = []
    for i in range(len(strings)):
        string = strings[i]
        encoded_string = encode_string(string, encoding_table)
        new_offsets.append(len(new_data))
        new_data += bytes.fromhex(encoded_string)
    new_offsets.append(len(new_data))
    return new_data, new_offsets

def write_offsets_strings(data, string_locations, strings):
    pass