import json
import os
from base64 import b64encode as b64e, b64decode as b64d

class SaveProvider:
    def __init__(self, slots: int, folder: str, file_name_pattern: str) -> None:
        self.slots: int = slots
        self.folder: str = folder
        self.file_name_pattern: str = file_name_pattern

    def _slot_file_name(self, slot):
        return os.path.join(self.folder, self.file_name_pattern.format(slot))

    def xor(self, text):
        key = "SaveProvider(self.SAVE_SLOTS, self.save_folder, 'mentes-{}.sav')"
        v1 = (key * (len(text) // len(key) + 1))[0:len(text)]
        v2 = text
        print(len(v1))
        print(len(v2))
        new = [chr(ord(a) ^ ord(b)) for a, b in zip(v1, v2)]
        return "".join(new)

    def load(self, slot):
        file_name: str = self._slot_file_name(slot)
        if not os.path.exists(file_name):
            raise Exception('A mentés fájl nem létezik.')

        data_file = open(file_name, "r")
        try:
            data = data_file.read()
            decr = b64d(data).decode('utf-8')
            obj = json.loads(decr)
            return obj
        finally:
            data_file.close()

    def save(self, slot, data):
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        file_name: str = self._slot_file_name(slot)

        data_file = open(file_name, "w")
        try:
            ser = json.dumps(data)
            encr = b64e(ser.encode('utf-8')).decode('utf-8')
            data_file.write(encr)
        finally:
            data_file.close()
