import struct
import os
import json
import random

with open("WLASL.json") as f:
    WORDDATA = json.load(f)

with open("meshes_v2.json") as f:
    MESHDATA = json.load(f)


class LandMarkReader:
    def __init__(self, filepath) -> None:
        self.file = open(filepath, "rb")
        self.info = {"face": (0, 67), "pose": (67, 33), "rhand": (100, 21), "lhand": (121, 21)}
        self.size = os.path.getsize(filepath) // 4
        self.num_frames = self.size // 71

    def get(self, part, frame, point_index, multiplier=1):
        offset = self.info[part][0] * 4 * self.size // 142
        offset += self.info[part][1] * 2 * frame
        offset += point_index << 1

        cursor = offset >> 2
        shamt = offset & 3

        self.file.seek(cursor * 4)
        bin_data = self.file.read(4)
        num = struct.unpack("I", bin_data)[0]

        return [
            ((num >> (shamt * 8)) & 255) * multiplier,
            ((num >> ((shamt + 1) * 8)) & 255) * multiplier,
        ]

    def get_numpoints(self, part):
        return self.info[part][1]

    def close(self):
        self.file.close()


class WordReader(LandMarkReader):
    def __init__(self, word) -> None:
        filepath = random.choice(WORDDATA[word])
        filepath = f"landmarks_v5/{filepath['video_id']}.bin"
        super().__init__(filepath)
