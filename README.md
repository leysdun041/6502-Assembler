# 6502-Assembler

A assembler for the 6502 assembly language written in python. This is still a WIP so it might not work fully.

# Assembling

Run with command:
python3 assemble.py <filename.s>

# How to program

Sample code is shown in the samples directory.

Define a marker like this and loop to the marker

;Comment
foo:
lda #$00
jmp foo

Comments begin in a ";".

Be sure that all instructions are capitalized or it will error. 

# Future additions

I will add .ORG and .BYTE in the future. 

