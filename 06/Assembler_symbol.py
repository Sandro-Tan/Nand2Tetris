import re
from Dec2Bin import Dec2Bin
from Comp import Comp
from Dest import Dest
from Jump import Jump
from Code_cleaner import Code_cleaner

SYMBOL = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9,
           'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15, 'SCREEN':16384, 'KBD':24576,
           'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4}

FILES = ('add.asm', 'Max.asm', 'MaxL.asm','Pong.asm', 'PongL.asm', 'Rect.asm','RectL.asm')

for file in FILES:
    with open(file, 'r') as asm:
        asm_clean = []
        for line in asm.readlines():
            if Code_cleaner(line) != '':
                asm_clean.append(Code_cleaner(line))

        binary_ins = [] # final output
        i = 0           # label symbols count
        n = 16          # start address of user variables

        # Add label symbols to SYMBOL
        for ins in asm_clean:
            if ins.startswith('('):
                SYMBOL[ins[1:-1]] = asm_clean.index(ins) - i
                i += 1

        # Processing
        for ins in asm_clean:

            # Translate existing symbol A-instructions ('R0')
            if ins in SYMBOL:
                binary_ins.append(Dec2Bin(SYMBOL[ins]) + '\n')

            # Translate pure number A-instructions ('0')
            elif (ins not in SYMBOL) and (re.findall('^[0-9]+$', ins)):
                binary_ins.append(Dec2Bin(int(ins)) + '\n')

            # Translate new variable symbol A-instructions ('address')
            elif (ins not in SYMBOL) and (re.findall('^[a-z]+', ins)):
                    SYMBOL[ins] = n
                    binary_ins.append(Dec2Bin(n) + '\n')
                    n += 1

            # Translate C-instructions ('D=M', '0;JMP')
            elif (ins not in SYMBOL) and (re.findall('^[0-9A-Z]+', ins)):
                binary_ins.append(Comp(ins) + Dest(ins) + Jump(ins) + '\n')

        # Output
        file_assembled = file[0:-4] + '_assembled.hack'
        with open(file_assembled, 'w') as f:
            for ins in binary_ins:
                f.write(ins)
