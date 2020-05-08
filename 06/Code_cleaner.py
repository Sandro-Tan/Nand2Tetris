# Remove comments, spaces, and '@' at the start
import re

def Code_cleaner(str):
    if re.search('//', str):
        newstr = str.split('//')
        newstr = newstr[0]
        newstr = newstr.strip()
    else:
        newstr = str.strip()

    if newstr.startswith('@'):
        newstr = newstr[1:]

    return newstr


# test_cases = ['   0;JMP            // goto output_d',
#               '// Computes R2 = max(R0, R1)  (R0,R1,R2 refer to RAM[0],RAM[1],RAM[2])',
#               '   M=D              // M[2] = D (greatest number)',
#               '   @R0',
#               '(OUTPUT_FIRST)']
# for case in test_cases:
#     print(Code_clean(case))