@111
D=A
@SP
A=M
M=D
@SP
M=M+1
//////////////push constant 111
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
//////////////push constant 333
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
//////////////push constant 888
@SP
M=M-1
@SP
A=M
D=M
@Foo.8
M=D
//////////////pop static 8
@SP
M=M-1
@SP
A=M
D=M
@Foo.3
M=D
//////////////pop static 3
@SP
M=M-1
@SP
A=M
D=M
@Foo.1
M=D
//////////////pop static 1
@Foo.3
D=M
@SP
A=M
M=D
@SP
M=M+1
//////////////push static 3
@Foo.1
D=M
@SP
A=M
M=D
@SP
M=M+1
//////////////push static 1
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
@Foo.8
D=M
@SP
A=M
M=D
@SP
M=M+1
//////////////push static 8
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