// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//=============================================//
(RESTART)
@SCREEN
D=A 
@R0
M=D		// Set R0 = 16384


//=============================================//
(KBDCHECK)
@KBD
D=M
@WHITE
D;JEQ
@BLACK
D;JGT
@KBDCHECK
0;JMP


//=============================================//
(WHITE)
@R1
M=0
@DRAW
0;JMP

(BLACK)
@R1
M=-1
@DRAW
0;JMP

//=============================================//
(DRAW)
@R1
D=M			// D = color

@R0			
A=M			// A = 16384
M=D			// Draw at 16384

@R0			// A = 0
M=M+1		// R0++
D=M

@KBD		
D=D-A		// R0 - 24576

@DRAW
D;JLT

@RESTART
0;JMP