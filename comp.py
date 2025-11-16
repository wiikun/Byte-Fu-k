import sys
import re
import os

if len(sys.argv) < 2:
    print(f"usage:python {sys.argv[0]} file.fasm")
    sys.exit(1)
    
TABLE = {
    "add":0x00,
    "sub":0x01,
    "rig":0x02,
    "lef":0x03,
    "loop":0x04,
    "end":0x05,
    "putc":0x06,
    "getc":0x07
}

OPTAB = {
    "add",
    "sub",
    "rig",
    "lef"
}
    
with open(sys.argv[1]) as file:
    ST = [j.split(" ") for j in file.read().split("\n")]

LENG = len(ST)
RES = bytearray()
i = 0

while(LENG > i):
    RES.append(TABLE[ST[i][0]])
    if ST[i][0] in OPTAB:
        RES.append(int(ST[i][1]))
    i += 1

with open(os.path.splitext(os.path.basename(sys.argv[1]))[0] + ".bin","wb") as file:
    file.write(RES)