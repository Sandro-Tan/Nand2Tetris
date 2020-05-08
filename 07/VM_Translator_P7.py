'''
This python script can translate VM source code into Hack assembly code
and output in a .asm file

Author: Sandro Tan
Contact: sandro.tan@hotmail.com
Date: 23 Apr 2020
Version: 1.0
'''

# Two dictionaries that store segment symbols, simplifying the code

SEGMENT_POINTER = {
    'local': 'LCL',
    'this': 'THIS',
    'that': 'THAT',
    'argument': 'ARG'
}

POINTER = {
    '0': 'THIS',
    '1': 'THAT'
}


class Parser:
    def __init__(self, vmfile):
        # Open a vm file
        try:
            self.input = open(vmfile, 'r')
            self.currentCommand = None

        except:
            print('Invalid file input')

    def hasMoreCommands(self):
        line = self.input.readline()

        if line:  # load a line
            self.currentCommand = line
            return True

        if not line:  # end of file or blank line
            self.currentCommand = None
            return False

    def advance(self):
        if self.hasMoreCommands():
            s = self.currentCommand.split('//')
            if len(s[0]) > 1:  # true command line
                self.currentCommand = s[0]
            else:  # recursion: if comment line, go to next line
                self.advance()

    def print(self):
        print(self.currentCommand, type(self.currentCommand))

    def get_currentCommand(self):
        return self.currentCommand

    def commandType(self):
        c_type = None

        if self.currentCommand:
            if self.currentCommand.startswith('push'):
                c_type = 'C_PUSH'
            elif self.currentCommand.startswith('pop'):
                c_type = 'C_POP'
            elif self.currentCommand == 'return':
                c_type = 'C_RETURN'
            elif self.currentCommand.startswith('label'):
                c_type = 'C_LABEL'
            elif self.currentCommand.startswith('function'):
                c_type = 'C_FUNCTION'
            elif self.currentCommand.startswith('call'):
                c_type = 'C_CALL'
            elif self.currentCommand.startswith('if-goto'):
                c_type = 'C_IF'
            elif self.currentCommand.startswith('goto'):
                c_type = 'C_GOTO'
            elif len(self.currentCommand) > 1:
                c_type = 'C_ARITHMETIC'

        return c_type

    def arg1(self):
        argu1 = self.commandType()

        if argu1 and argu1 != 'C_RETURN':

            if argu1 == 'C_ARITHMETIC':
                return self.currentCommand.strip()  # return the command itself (add, sub, etc)

            else:
                return self.currentCommand.split(' ')[1]  # return the 1st argument (constant, static, etc)

    def arg2(self):
        arg2_list = ('C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL')
        argu2 = self.commandType()

        if argu2 in arg2_list:
            return self.currentCommand.split(' ')[2].strip()  # return an integer


class CodeWriter:
    def __init__(self, asmfile):
        ''''
        Create a new asm file to write assembly code, line by line
        '''
        self.output = open(asmfile, 'w')
        self.eq_count = 0
        self.gt_count = 0
        self.lt_count = 0

    def writeArithmetic(self, command):
        '''
        Receive a Parser object and if it is an arithmetic command,
        translate it into assembly code, and write in output file
        :param command: A Parser object
        :return: None
        '''

        result = []

        '''
        To ensure correct execution sequence, 
        these counters will be encoded into the final assembly code
        '''

        # Functions begin here
        if command.commandType() == 'C_ARITHMETIC':
            if command.arg1() == 'add':
                result = [
                    '@SP',
                    'M=M-1',  # SP--
                    'A=M-1',
                    'D=M',  # D = *(SP-1)
                    '@temp',
                    'M=D',
                    '@SP',
                    'A=M',
                    'D=M',  # D = *SP
                    '@temp',
                    'M=D+M', # !!!!!!
                    'D=M',  # D = *SP + *(SP-1)
                    '@SP',
                    'A=M-1',
                    'M=D',  # *SP = D
                    '//////////////' + command.get_currentCommand().strip()
                ]

            elif command.arg1() == 'sub':
                result = [
                    '@SP',
                    'M=M-1',
                    'A=M-1',
                    'D=M',  # D = *(SP-1)
                    '@temp',
                    'M=D',
                    '@SP',
                    'A=M',
                    'D=M',  # D = *SP
                    '@temp',
                    'M=M-D', # !!!!!!
                    'D=M',
                    '@SP',
                    'A=M-1',
                    'M=D',
                    '//////////////' + command.get_currentCommand().strip()
                ]

            elif command.arg1() == 'neg':
                result = [
                    '@SP',
                    'A=M-1',
                    'M=-M',  # *(SP-1) = -*(SP-1)
                    '//////////////' + command.get_currentCommand().strip()
                ]

            elif command.arg1() == 'eq':
                self.eq_count += 1
                result = [
                    '@SP',
                    'M=M-1',  # SP--
                    'A=M',
                    'D=M',  # D = *SP
                    '@temp',
                    'M=D',  # temp = D
                    '@SP',
                    'A=M-1',
                    'D=M',  # D = *(SP-1)
                    '@temp',
                    'M=D-M',  # temp = *(SP-1) - *SP
                    'D=M',

                    '@EQ' + str(self.eq_count),
                    'D;JEQ',
                    '@NOT_EQ' + str(self.eq_count),
                    'D;JNE',

                    '(EQ' + str(self.eq_count) + ')',
                    '@SP',
                    'A=M-1',
                    'M=-1',  # set result = -1, *(SP-1) == *SP
                    '@EQ_END' + str(self.eq_count),
                    '0;JMP',

                    '(NOT_EQ' + str(self.eq_count) + ')',
                    '@SP',
                    'A=M-1',
                    'M=0',  # set result = 0, *(SP-1) != *SP
                    '@EQ_END' + str(self.eq_count),
                    '0;JMP',

                    '(EQ_END' + str(self.eq_count) + ')',

                    '//////////////' + command.get_currentCommand().strip()

                ]

            elif command.arg1() == 'gt':
                self.gt_count += 1
                result = [
                    '@SP',
                    'M=M-1',  # SP--
                    'A=M',
                    'D=M',  # D = *SP
                    '@temp',
                    'M=D',  # temp = D
                    '@SP',
                    'A=M-1',
                    'D=M',  # D = *(SP-1)
                    '@temp',
                    'M=D-M',  # temp = *(SP-1) - *SP
                    'D=M',

                    '@GT' + str(self.gt_count),
                    'D;JGT',
                    '@NOT_GT' + str(self.gt_count),
                    'D;JLE',

                    '(GT' + str(self.gt_count) + ')',
                    '@SP',
                    'A=M-1',
                    'M=-1',  # set result = -1, *(SP-1) > *SP
                    '@GT_END' + str(self.gt_count),
                    '0;JMP',

                    '(NOT_GT' + str(self.gt_count) + ')',
                    '@SP',
                    'A=M-1',
                    'M=0',  # set result = 0, *(SP-1) <= *SP
                    '@GT_END' + str(self.gt_count),
                    '0;JMP',

                    '(GT_END' + str(self.gt_count) + ')',

                    '//////////////' + command.get_currentCommand().strip()
                ]

            elif command.arg1() == 'lt':
                self.lt_count += 1
                result = [
                    '@SP',
                    'M=M-1',  # SP--
                    'A=M',
                    'D=M',  # D = *SP
                    '@temp',
                    'M=D',  # temp = D
                    '@SP',
                    'A=M-1',
                    'D=M',  # D = *(SP-1)
                    '@temp',
                    'M=D-M',  # temp = *(SP-1) - *SP
                    'D=M',

                    '@LT' + str(self.lt_count),
                    'D;JLT',
                    '@NOT_LT' + str(self.lt_count),
                    'D;JGE',

                    '(LT' + str(self.lt_count) + ')',
                    '@SP',
                    'A=M-1',
                    'M=-1',  # set result = -1, *(SP-1) < *SP
                    '@LT_END' + str(self.lt_count),
                    '0;JMP',
                    '(NOT_LT' + str(self.lt_count) + ')',
                    '@SP',
                    'A=M-1',
                    'M=0',  # set result = 0, *(SP-1) >= *SP
                    '@LT_END' + str(self.lt_count),
                    '0;JMP',

                    '(LT_END' + str(self.lt_count) + ')',

                    '//////////////' + command.get_currentCommand().strip()
                ]

            elif command.arg1() == 'and':
                result = [
                    '@SP',
                    'M=M-1',  # SP--
                    'A=M',
                    'D=M',  # D = *SP
                    '@temp',
                    'M=D',  # temp = D
                    '@SP',
                    'A=M-1',
                    'D=M',  # D = *(SP-1)
                    '@temp',
                    'M=D&M',  # temp = *(SP-1) & *SP
                    'D=M',
                    '@SP',
                    'A=M-1',
                    'M=D',  # *(SP-1) = temp

                    '//////////////' + command.get_currentCommand().strip()
                ]

            elif command.arg1() == 'or':
                result = [
                    '@SP',
                    'M=M-1',  # SP--
                    'A=M',
                    'D=M',  # D = *SP
                    '@temp',
                    'M=D',  # temp = D
                    '@SP',
                    'A=M-1',
                    'D=M',  # D = *(SP-1)
                    '@temp',
                    'M=D|M',  # temp = *(SP-1) | *SP
                    'D=M',
                    '@SP',
                    'A=M-1',
                    'M=D',  # *(SP-1) = temp

                    '//////////////' + command.get_currentCommand().strip()
                ]

            elif command.arg1() == 'not':
                result = [
                    '@SP',
                    'A=M-1',
                    'D=!M',  # D = !*(SP-1)
                    '@SP',
                    'A=M-1',
                    'M=D',  # *(SP-1) = D

                    '//////////////' + command.get_currentCommand().strip()
                ]

        # Add new line symbol to each line and write file
        result = [line + '\n' for line in result]
        for line in result:
            self.output.write(line)

    def writePushPop(self, command, segment, index):
        '''
        Receive a Parser object and if it is a push/pop command,
        translate it into assembly code, and write in output file
        :param command: A Parser object
        :param segment: The segment part of a command, e.g, constant/local/static
        :param index: The location part of a command; an integer
        :return: None
        '''

        result = []

        # Functions begin here
        if command.commandType() == 'C_PUSH' and segment == 'constant':
            result = [
                '@' + index,
                'D=A',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1',  # SP++
                '//////////////' + command.get_currentCommand().strip()
            ]

        elif command.commandType() == 'C_POP' and segment in SEGMENT_POINTER:
            result = [
                '@' + index,
                'D=A',  # D = i
                '@addr',
                'M=D',  # addr = D = i
                '@' + SEGMENT_POINTER[segment],
                'D=M',  # D = segment pointer value
                '@addr',
                'M=D+M',  # addr = segment pointer value + i
                '@SP',  # SP--
                'M=M-1',
                '@SP',  # *addr = *SP
                'A=M',
                'D=M',
                '@addr',
                'A=M',
                'M=D',
                '//////////////' + command.get_currentCommand().strip()
            ]

        elif command.commandType() == 'C_PUSH' and segment in SEGMENT_POINTER:
            result = [
                '@' + index,  ## addr = seg + i
                'D=A',
                '@addr',
                'M=D',
                '@' + SEGMENT_POINTER[segment],
                'D=M',
                '@addr',
                'M=D+M',
                '@addr',  ## *SP = *addr
                'A=M',
                'D=M',
                '@SP',
                'A=M',
                'M=D',
                '@SP',  ## SP++
                'M=M+1',
                '//////////////' + command.get_currentCommand().strip()
            ]

        elif command.commandType() == 'C_POP' and segment == 'temp':
            result = [
                '@' + index,  ## addr = 5 + i
                'D=A',
                '@addr',
                'M=D',
                '@5',
                'D=A',
                '@addr',
                'M=D+M',
                '@SP',
                'M=M-1',  ## SP--
                '@SP',  ## *addr = *SP
                'A=M',
                'D=M',
                '@addr',
                'A=M',
                'M=D',
                '//////////////' + command.get_currentCommand().strip()
            ]

        elif command.commandType() == 'C_PUSH' and segment == 'temp':
            result = [
                '@' + index,  ## addr = 5 + i
                'D=A',
                '@addr',
                'M=D',
                '@5',
                'D=A',
                '@addr',
                'M=D+M',
                '@addr',  ## *SP = *addr
                'A=M',
                'D=M',
                '@SP',
                'A=M',
                'M=D',
                '@SP',  ## SP++
                'M=M+1',
                '//////////////' + command.get_currentCommand().strip()
            ]

        elif command.commandType() == 'C_POP' and segment == 'pointer':
            result = [
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                '@' + POINTER[index],
                'M=D',
                '//////////////' + command.get_currentCommand().strip()
            ]

        elif command.commandType() == 'C_PUSH' and segment == 'pointer':
            result = [
                '@' + POINTER[index],
                'D=M',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1',
                '//////////////' + command.get_currentCommand().strip()
            ]

        elif command.commandType() == 'C_POP' and segment == 'static':
            result = ['@SP',
                      'M=M-1',  # SP--
                      '@SP',
                      'A=M',
                      'D=M',  # D=*SP
                      '@Foo.' + index,
                      'M=D',  # Foo = D
                      '//////////////' + command.get_currentCommand().strip()
                      ]

        elif command.commandType() == 'C_PUSH' and segment == 'static':
            result = ['@Foo.' + index,
                      'D=M',  # D = Foo
                      '@SP',
                      'A=M',
                      'M=D',  # *SP = D
                      '@SP',
                      'M=M+1',  # SP++
                      '//////////////' + command.get_currentCommand().strip()
                      ]

        # Add new line symbol to each line and write file
        result = [line + '\n' for line in result]
        for line in result:
            self.output.write(line)

    def close(self):
        '''
        close the output asm file
        '''
        self.output.close()


def main():
    '''
    The main driver of the whole translation process
    :return: None
    '''
    filenames = ('StaticTest.vm', 'PointerTest.vm', 'BasicTest.vm', 'SimpleAdd.vm', 'StackTest.vm')
    for filename in filenames:
        test_read = Parser(filename)
        test_write = CodeWriter(filename[:-3] + '.asm')

        while True:
            test_write.writeArithmetic(test_read)
            test_write.writePushPop(test_read, test_read.arg1(), test_read.arg2())
            if not test_read.hasMoreCommands():
                test_write.close()
                break


# Get things rolling
main()
