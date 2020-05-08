# Parse the string before '='

import re

DEST = {'null':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101','AD':'110', 'AMD':'111'}

def Dest(str):
    if re.search('=', str):
        newstr = str.split('=')
        newstr = newstr[0]
    else:
        newstr = 'null'
    return DEST[newstr]

# test_cases = ['MD=D+1', '0;JMP', 'M=D']
# for case in test_cases:
#     print(Dest(case))
# # 011, 000, 001 #