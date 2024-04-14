from cProfile import label
import re
import sys


bytecode = b""
labels = []
jmps = []
print(sys.argv)

def nums_to_bytes(nums:str) -> bytes:
    assert(len(nums) == 8)
    bstring = b""
    for byte in [nums[i:i+2] for i in range(0, len(nums), 2)]:
        bstring += b"%c"%(int(byte,16))
    assert(len(bstring) == 4)
    return bstring

def find_label(label:str, labels:list) -> int:
    ret = 0
    for item in labels:
        if item[1] == label:
            ret = item[0]
    return ret

with open(sys.argv[1], "r") as f:
    file = f.read().split("\n")
    under = ""
    for line in file:
        line = line.strip().rstrip(";")
        comma = line.find(",")
        if comma >= 0:
            line = line[:comma] + line[comma+1:]
        if line == "":
            continue
        elif ":" in line:
            under = line.rstrip(":")
            labels.append([len(bytecode),under])
        elif "mov" in line:
            operands = line.split()[1:]
            op1 = re.match("r[0-3]|r[a-z]{2}", operands[0])
            op2 = re.match("r[0-3]|r[a-z]{2}", operands[1])
            if (op1 is not None and op2 is not None):
                if operands[0] == "r0":
                    if operands[1] == "r1":
                        bytecode += b"\xc2\x12"
                    elif operands[1] == "r2":
                        bytecode += b"\xc2\x13"
                    elif operands[1] == "r3":
                        bytecode += b"\xc2\x14"
                    elif operands[1] == "rsp":
                        bytecode += b"\xc2\x15"
                    elif operands[1] == "rbp":
                        bytecode += b"\xc2\x16"
                    elif operands[1] == "rip":
                        bytecode += b"\xc2\x17"
                elif operands[0] == "r1":
                    if operands[1] == "r0":
                        bytecode += b"\xc2\x21"
                    elif operands[1] == "r2":
                        bytecode += b"\xc2\x23"
                    elif operands[1] == "r3":
                        bytecode += b"\xc2\x24"
                    elif operands[1] == "rsp":
                        bytecode += b"\xc2\x25"
                    elif operands[1] == "rbp":
                        bytecode += b"\xc2\x26"
                    elif operands[1] == "rip":
                        bytecode += b"\xc2\x27"
                elif operands[0] == "r2":
                    if operands[1] == "r0":
                        bytecode += b"\xc2\x31"
                    elif operands[1] == "r1":
                        bytecode += b"\xc2\x32"
                    elif operands[1] == "r3":
                        bytecode += b"\xc2\x34"
                    elif operands[1] == "rsp":
                        bytecode += b"\xc2\x35"
                    elif operands[1] == "rbp":
                        bytecode += b"\xc2\x36"
                    elif operands[1] == "rip":
                        bytecode += b"\xc2\x37"
                elif operands[0] == "r3":
                    if operands[1] == "r0":
                        bytecode += b"\xc2\x41"
                    elif operands[1] == "r1":
                        bytecode += b"\xc2\x42"
                    elif operands[1] == "r2":
                        bytecode += b"\xc2\x43"
                    elif operands[1] == "rsp":
                        bytecode += b"\xc2\x45"
                    elif operands[1] == "rbp":
                        bytecode += b"\xc2\x46"
                    elif operands[1] == "rip":
                        bytecode += b"\xc2\x47"
                elif operands[0] == "rsp":
                    if operands[1] == "r0":
                        bytecode += b"\xc2\x51"
                    elif operands[1] == "r1":
                        bytecode += b"\xc2\x52"
                    elif operands[1] == "r2":
                        bytecode += b"\xc2\x53"
                    elif operands[1] == "r3":
                        bytecode += b"\xc2\x54"
                    elif operands[1] == "rbp":
                        bytecode += b"\xc2\x56"
                    elif operands[1] == "rip":
                        bytecode += b"\xc2\x57"
                elif operands[0] == "rbp":
                    if operands[1] == "r0":
                        bytecode += b"\xc2\x61"
                    elif operands[1] == "r1":
                        bytecode += b"\xc2\x62"
                    elif operands[1] == "r2":
                        bytecode += b"\xc2\x63"
                    elif operands[1] == "r3":
                        bytecode += b"\xc2\x64"
                    elif operands[1] == "rsp":
                        bytecode += b"\xc2\x65"
                    elif operands[1] == "rip":
                        bytecode += b"\xc2\x67"
                elif operands[0] == "rip":
                    if operands[1] == "r0":
                        bytecode += b"\xc2\x71"
                    elif operands[1] == "r1":
                        bytecode += b"\xc2\x72"
                    elif operands[1] == "r2":
                        bytecode += b"\xc2\x73"
                    elif operands[1] == "r3":
                        bytecode += b"\xc2\x74"
                    elif operands[1] == "rsp":
                        bytecode += b"\xc2\x75"
                    elif operands[1] == "rbp":
                        bytecode += b"\xc2\x76"
            elif (op1 is not None):
                if operands[1] == "mem":
                    if operands[0] == "r0":
                        bytecode += b"\xc3\xf1\x01"
                    elif operands[0] == "r1":
                        bytecode += b"\xc3\xf1\x02"
                    elif operands[0] == "r2":
                        bytecode += b"\xc3\xf1\x03"
                    elif operands[0] == "r3":
                        bytecode += b"\xc3\xf1\x04"
                    elif operands[0] == "rsp":
                        bytecode += b"\xc3\xf1\x05"
                    elif operands[0] == "rbp":
                        bytecode += b"\xc3\xf1\x06"
                    elif operands[0] == "rip":
                        bytecode += b"\xc3\xf1\x07"
                elif operands[1].isalpha():
                    jmps.append([len(bytecode), under,operands[1]])
                else:
                    if operands[0] == "r0":
                        bytecode += b"\xc2\xcf\x01" + nums_to_bytes(operands[1])
                    elif operands[0] == "r1":
                        bytecode += b"\xc2\xcf\x02" + nums_to_bytes(operands[1])
                    elif operands[0] == "r2":
                        bytecode += b"\xc2\xcf\x03" + nums_to_bytes(operands[1])
                    elif operands[0] == "r3":
                        bytecode += b"\xc2\xcf\x04" + nums_to_bytes(operands[1])
                    elif operands[0] == "rsp":
                        bytecode += b"\xc2\xcf\x05" + nums_to_bytes(operands[1])
                    elif operands[0] == "rbp":
                        bytecode += b"\xc2\xcf\x06" + nums_to_bytes(operands[1])
                    elif operands[1] == "rip":
                        bytecode += b"\xc2\xcf\x07" + nums_to_bytes(operands[1])
            else:
                if operands[0] == "mem":
                    if operands[1] == "r0":
                        bytecode += b"\xc3\x01\xf1"
                    elif operands[1] == "r1":
                        bytecode += b"\xc3\x02\xf1"
                    elif operands[1] == "r2":
                        bytecode += b"\xc3\x03\xf1"
                    elif operands[1] == "r3":
                        bytecode += b"\xc3\x04\xf1"
                    elif operands[1] == "rsp":
                        bytecode += b"\xc3\x05\xf1"
                    elif operands[1] == "rbp":
                        bytecode += b"\xc3\x06\xf1"
                    elif operands[1] == "rip":
                        bytecode += b"\xc3\x07\xf1"
                else:
                    continue
        elif "push" in line:
            operands = line.split()[1:]
            if operands[0] == "r0":
                bytecode += b"\xc0\x01"
            elif operands[0] == "r1":
                bytecode += b"\xc0\x02"
            elif operands[0] == "r2":
                bytecode += b"\xc0\x03"
            elif operands[0] == "r3":
                bytecode += b"\xc0\x04"
            elif operands[0] == "rsp":
                bytecode += b"\xc0\x05"
            elif operands[0] == "rbp":
                bytecode += b"\xc0\x06"
            else:
                bytecode += b"\xc0\x07"
        elif "sub" in line:
            bytecode += b"\xac\xb2"
        elif "jmp" in line:
            bytecode += b"\xbb\xc6"
        elif "scanf" in line:
            bytecode += b"\xd6\xff"
        elif "readfile" in line:
            bytecode += b"\xc7\xff"
        elif "read" in line:
            bytecode += b"\xd7\xff"
        elif "call" in line:
            bytecode += b"\xcc\x8f"
        elif "leave" in line:
            bytecode += b"\xc2\xf0"
        elif "ret" in line:
            bytecode += b"\xc2\xf8"
        elif "cmp" in line:
            bytecode += b"\xd5\xff"
        elif "jne" in line:
            bytecode += b"\xbb\xc3"
        elif "print":
            bytecode += b"\xd8\xff"
        else:
            print(line)
    for i in range(len(jmps)):
        for j in range(i+1, len(jmps)):
            jmps[j][0] += 7
        flag = False
        for j in range(len(labels)):
            if jmps[i][1] == labels[j][1]:
                print(jmps[i][1])
                flag = True
            elif flag:
                labels[j][0] += 7
    for i in range(len(jmps)):
        bytecode = bytecode[:jmps[i][0]] + b"\xc2\xcf\x04" + nums_to_bytes(f"{find_label(jmps[i][2], labels) + 0x400000:08x}") + bytecode[jmps[i][0]:]
    print(labels)
    print(jmps)
print(bytecode)
for i in range(len(labels)):
    if i == len(labels) - 1:
        print(f"{labels[i][1]}:\n{bytecode[labels[i][0]:]}")
    else:
        print(f"{labels[i][1]}:\n{bytecode[labels[i][0]:labels[i+1][0]]}")
if len(sys.argv) > 2:
    for file in sys.argv[2:]:
        with open(file, "wb") as f:
            f.write(bytecode)
    