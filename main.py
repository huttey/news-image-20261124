#!/usr/bin/env python3
"""Copy the entry image to /output/entry.png (no network).

Validates the gate before copying: a whole PNG or JPEG, at most
1 MiB, at most 1024x1024 pixels. Standard library only.
"""
import os
import shutil
import struct

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                   "entry.png")


def gate_ok(data):
    """True when data is a whole PNG or JPEG within the gate."""
    if len(data) > 1048576:
        return False
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        width, height = struct.unpack(">II", data[16:24])
        return width <= 1024 and height <= 1024
    if data[:2] == b"\xff\xd8" and data[-2:] == b"\xff\xd9":
        return True
    return False


with open(SRC, "rb") as f:
    data = f.read()
assert gate_ok(data), "entry.png fails the gate"
os.makedirs(os.path.dirname(DST), exist_ok=True)
shutil.copyfile(SRC, DST)
