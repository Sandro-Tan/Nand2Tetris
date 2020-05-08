# Parse the string after ';'

import re

JUMP = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}

def Jump(str):
    if re.search(';', str):
        newstr = str.split(';')
        newstr = newstr[1]
    else:
        newstr = 'null'
    return JUMP[newstr]

# test_cases = ['MD=D+1;JGE', '0;JMP', 'M=D']
# for case in test_cases:
#     print(Jump(case))
# # 011, 111, 000 #