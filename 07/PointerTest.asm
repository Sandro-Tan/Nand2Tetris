@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
//////////////push constant 3030
@SP
M=M-1
A=M
D=M
@THIS
M=D
//////////////pop pointer 0
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
//////////////push constant 3040
@SP
M=M-1
A=M
D=M
@THAT
M=D
//////////////pop pointer 1
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
//////////////push constant 32
@2
D=A
@addr
M=D
@THIS
D=M
@addr
M=D+M
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
//////////////pop this 2
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
//////////////push constant 46
@6
D=A
@addr
M=D
@THAT
D=M
@addr
M=D+M
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
//////////////pop that 6
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//////////////push pointer 0
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//////////////push pointer 1
@SP
M=M-1
A=M-1
D=M
@temp
M=D
@SP
A=M
D=M
@temp
M=D+M
D=M
@SP
A=M-1
M=D
//////////////add
@2
D=A
@addr
M=D
@THIS
D=M
@addr
M=D+M
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
//////////////push this 2
@SP
M=M-1
A=M-1
D=M
@temp
M=D
@SP
A=M
D=M
@temp
M=M-D
D=M
@SP
A=M-1
M=D
//////////////sub
@6
D=A
@addr
M=D
@THAT
D=M
@addr
M=D+M
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
//////////////push that 6
@SP
M=M-1
A=M-1
D=M
@temp
M=D
@SP
A=M
D=M
@temp
M=D+M
D=M
@SP
A=M-1
M=D
//////////////add
