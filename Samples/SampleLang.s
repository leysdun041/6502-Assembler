;Comment
.ORG $1000
BRK
BPL hi

token:
LDA ($3),y
LDA token
LDA $3
hi:
LDA #$3
LDA (3),x
