import sys

if len(sys.argv) < 2:
    print(f"usage:python {sys.argv[0]} file.byf")
    sys.exit(1)

slot = [0x00 for _ in range(3000)]
ptr = 0
jmpMap = {}
mapStack = []
jmpI = []
index = 0
buf = []

#ハンドラここから

def inc(arg):
    val = slot[ptr]
    slot[ptr] = val + arg
    
def dec(arg):
    val = slot[ptr]
    slot[ptr] = val - arg

def ptf(arg):
    global ptr
    ptr += arg
    
def ptb(arg):
    global ptr
    ptr -= arg
    
def lpStr():
    global index
    if not slot[ptr]:
        index = jmpMap[index] + 1

def lpEnd():
    global index
    if slot[ptr]:
        index = jmpMap[index]

def prt():
    print(chr(slot[ptr]) ,end="")

def ipt():
    global slot,ptr,buf
    if len(buf) < 1:
        buf = [i for i in input()] + ["\n","\0"]
    if buf:
        slot[ptr] = ord(buf.pop(0))
    else:
        slot[ptr] = int(00)

TABLE = {
    0x00:inc,
    0x01:dec,
    0x02:ptf,
    0x03:ptb,
    0x04:lpStr,
    0x05:lpEnd,
    0x06:prt,
    0x07:ipt
}

OPTAB = {
    0x00,
    0x01,
    0x02,
    0x03
}

#ここまで

with open(sys.argv[1],"rb") as file:
    CODE = bytearray(file.read())
    
    for i,code in enumerate(CODE):
        if code == 0x04:
            mapStack.append(i)
        elif code == 0x05:
            if not mapStack:
                print("\nerror not found match \"[\" at {} byte".format(i))
            start = mapStack.pop()
            jmpMap[start] = i
            jmpMap[i] = start 
    if mapStack:
        print("error not found match \"]\" at {} byte".format(i))

while len(CODE) > index:
    code = CODE[index]
    if code in TABLE:
        if code in OPTAB:
            TABLE[code](CODE[index + 1])
            index += 2
            continue
        else:
            TABLE[code]()
    else:
        print("error {} byte instruction is not found".format(index + 1))
    
    index += 1