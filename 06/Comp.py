# Parse the string between '=' and ';'

import re

# a = 0
COMP_0 = {'0':'101010',
        '1':'111111',
        '-1':'111010',
        'D':'001100',
        'A':'110000',
        '!D':'001101',
        '!A':'110001',
        '-D':'001111',
        '-A':'110011',
        'D+1':'011111',
        'A+1':'110111',
        'D-1':'001110',
        'A-1':'110010',
        'D+A':'000010',
        'D-A':'010011',
        'A-D':'000111',
        'D&A':'000000',
        'D|A':'010101'
}

# a = 1
COMP_1 = {'M':'110000',
          '!M':'110001',
          '-M':'110011',
          'M+1':'110111',
          'M-1':'110010',
          'D+M':'000010',
          'D-M':'010011',
          'M-D':'000111',
          'D&M':'000000',
          'D|M':'010101'

}

def Comp(str):
    newstr = str.split(';')
    newstr = newstr[0]
    if re.search('=', newstr):
        newstr = newstr.split('=')
        newstr = newstr[1]

    if re.search('M', newstr):
        return '1111' + COMP_1[newstr]
    else:
        return '1110' + COMP_0[newstr]

# test_cases = ['MD=D-M', '0;JMP', 'M=D']
# for case in test_cases:
#     print(Comp(case))