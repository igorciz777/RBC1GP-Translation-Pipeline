import struct


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
        start_offset = struct.unpack(endian + 'I', data[current_file_offset:current_file_offset + 4])[0]
        try:
            end_offset = struct.unpack(endian + 'I', data[current_file_offset + 4:current_file_offset + 8])[0]
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
    i = 0
    while i < len(input_string):
        matched = False

        if i + 1 < len(input_string):
            pair = input_string[i:i + 2]
            if pair in decoding_table:
                encoded_bytes += decoding_table[pair]
                i += 2
                matched = True
                continue

        char = input_string[i]
        if char == " ":
            char = "ASCII_SPACE"
        if char == "　":
            char = "EUCJP_SPACE"
        if char in decoding_table:
            encoded_bytes += decoding_table[char]
            matched = True
        else:
            i += 1
        if matched:
            i += 1
    return encoded_bytes





def write_offsets_strings(data, string_locations, strings):
    pass
