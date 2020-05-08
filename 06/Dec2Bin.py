# convert decimal address to 16bit binary address

def Dec2Bin(num):
    bits = ''
    while num >= 1:
        bit = num % 2
        num = int(num / 2)
        bits += str(bit)

    while len(bits) < 16:
        bits += '0'

    return ''.join(reversed(bits))

# test_cases = [0, 1, 2, 3, 10, 45, 69, 100]
# answers = ['0000000000000000', '0000000000000001', '0000000000000010',
#            '0000000000000011', '0000000000001010', '0000000000101101',
#            '0000000001000101', '0000000001100100']
#
# for i in range(len(test_cases)):
#     if Dec2Bin(test_cases[i]) == answers[i]:
#         print('Test', i+1, 'passed')
#         i += 1
#     if i == len(test_cases):
#         print('All passed')