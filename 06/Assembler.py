import re
from Dec2Bin import Dec2Bin
from Comp import Comp
from Dest import Dest
from Jump import Jump

SYMBOL = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9,
           'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15, 'Screen':16384, 'KBD':24576,
           'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4}

FILES = ('add.asm', 'MaxL.asm', 'PongL.asm', 'RectL.asm')

for file in FILES:
    asm = open(file, 'r')
    asm_clean = []

    for line in asm.readlines():
        if re.findall('^\S', line):  # exclude blank lines
            if not re.findall('^/', line): # exclude comment lines
                asm_clean.append(line.rstrip())

    binary_ins = []

    for ins in asm_clean:
        if ins.startswith('@'):
            addr = re.findall('[0-9]+', ins)
            binary_ins.append(Dec2Bin(int(addr[0])) + '\n')
        else:
            binary_ins.append(Comp(ins) + Dest(ins) + Jump(ins) + '\n')

    file_assembled = file[0:-4] + '_assembled.hack'
    with open(file_assembled, 'w') as f:
        for ins in binary_ins:
            f.write(ins)