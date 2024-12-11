# file reader for C1GP

import os
import struct

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QFrame


def check_max_length(text_edit, max_length):
    text = text_edit.toPlainText()

    if len(text) > max_length:
        text_edit.blockSignals(True)
        text_edit.setText(text[:max_length])
        text_edit.blockSignals(False)
        text_edit.moveCursor(QTextCursor.MoveOperation.End)


def highlight_too_long_lineedit(line_edit, hex_form, max_length):
    if len(hex_form) > max_length:
        line_edit.setStyleSheet("background-color: red")
    else:
        line_edit.setStyleSheet("background-color: white")


# defined structs
def rival_struct(file):
    rival_data = {
        'data_block0': file.read(0x214),
        'nickname': file.read(0x1A),
        'data_block1': file.read(0x52),
        'name': file.read(0x1A),
        'occupation': file.read(0x22),
        'motto': file.read(0x22),
        'profile_bio_1': file.read(0x42),
        'profile_bio_2': file.read(0x42),
        'profile_bio_3': file.read(0x42),
        'profile_bio_4': file.read(0x42),
        'profile_bio_5': file.read(0x42),
        'dialog_1': file.read(0x30),
        'dialog_2': file.read(0x30),
        'dialog_3': file.read(0x30),
        'dialog_4': file.read(0x30),
        'dialog_5': file.read(0x30),
        'dialog_6': file.read(0x30),
        'dialog_short_1': file.read(0x18),
        'dialog_short_2': file.read(0x18)
    }
    return rival_data


def team_struct(file):
    team = {
        'team_name': file.read(0x22)
    }
    return team


def event_struct(file):
    event = {
        'id': file.read_uint8(),
        'unk': file.read(0x4B),
        'event_name': file.read(0x1C)
    }
    return event


# class for reading binary files, little-endian
class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'r+b')
        self.file.seek(0, os.SEEK_END)
        self.file_size = self.file.tell()
        self.file.seek(0, os.SEEK_SET)

    def read(self, size):
        return self.file.read(size)

    def write_n_bytes(self, data, n):
        data = data.ljust(n, b'\x00')
        self.file.write(struct.pack('<' + 'B' * n, *data))

    def read_int8(self):
        return struct.unpack('<b', self.file.read(1))[0]

    def read_uint8(self):
        return struct.unpack('<B', self.file.read(1))[0]

    def read_int16(self):
        return struct.unpack('<h', self.file.read(2))[0]

    def read_uint16(self):
        return struct.unpack('<H', self.file.read(2))[0]

    def read_int32(self):
        return struct.unpack('<i', self.file.read(4))[0]

    def read_uint32(self):
        return struct.unpack('<I', self.file.read(4))[0]

    def read_int64(self):
        return struct.unpack('<q', self.file.read(8))[0]

    def read_uint64(self):
        return struct.unpack('<Q', self.file.read(8))[0]

    def read_float(self):
        return struct.unpack('<f', self.file.read(4))[0]

    def read_double(self):
        return struct.unpack('<d', self.file.read(8))[0]

    def seek(self, offset, whence=os.SEEK_SET):
        self.file.seek(offset, whence)

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()


class RivalFile:
    def __init__(self, filename):
        self.file = FileReader(filename)

    def get_rivals(self):
        rivals = []
        self.file.seek(0)
        for i in range(713):
            rival = rival_struct(self.file)
            rivals.append(rival)

        return rivals

    def write_rivals(self, rivals):
        self.file.seek(0)
        for rival in rivals:
            self.file.seek(0x214, os.SEEK_CUR)
            self.file.write_n_bytes(rival['nickname'], 0x1A)
            self.file.seek(0x52, os.SEEK_CUR)
            self.file.write_n_bytes(rival['name'], 0x1A)
            self.file.write_n_bytes(rival['occupation'], 0x22)
            self.file.write_n_bytes(rival['motto'], 0x22)
            self.file.write_n_bytes(rival['profile_bio_1'], 0x42)
            self.file.write_n_bytes(rival['profile_bio_2'], 0x42)
            self.file.write_n_bytes(rival['profile_bio_3'], 0x42)
            self.file.write_n_bytes(rival['profile_bio_4'], 0x42)
            self.file.write_n_bytes(rival['profile_bio_5'], 0x42)
            self.file.write_n_bytes(rival['dialog_1'], 0x30)
            self.file.write_n_bytes(rival['dialog_2'], 0x30)
            self.file.write_n_bytes(rival['dialog_3'], 0x30)
            self.file.write_n_bytes(rival['dialog_4'], 0x30)
            self.file.write_n_bytes(rival['dialog_5'], 0x30)
            self.file.write_n_bytes(rival['dialog_6'], 0x30)
            self.file.write_n_bytes(rival['dialog_short_1'], 0x18)
            self.file.write_n_bytes(rival['dialog_short_2'], 0x18)

    def get_teams(self):
        teams = []
        self.file.seek(0x000F3B38, os.SEEK_SET)
        for i in range(129):
            team = team_struct(self.file)
            teams.append(team)

        return teams

    def write_teams(self, teams):
        self.file.seek(0x000F3B38, os.SEEK_SET)
        for team in teams:
            self.file.write_n_bytes(team['team_name'], 0x22)

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()


class EventFile:
    def __init__(self, filename):
        self.file = FileReader(filename)

    def get_events(self):
        events = []
        self.file.seek(0x000006C0, os.SEEK_SET)
        for i in range(149):
            event = event_struct(self.file)
            events.append(event)

        return events

    def write_events(self, events):
        self.file.seek(0x000006C0, os.SEEK_SET)
        for event in events:
            self.file.seek(0x4C, os.SEEK_CUR)
            self.file.write_n_bytes(event['event_name'], 0x1C)

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()


class BADFile:
    def __init__(self, filename):
        self.file = FileReader(filename)

    def get_bad(self):
        # TODO implement
        bad = []
        return bad

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()
