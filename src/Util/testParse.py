a="""BRK impl ORA X,ind --- --- --- ORA zpg ASL zpg --- PHP impl ORA # ASL A --- --- ORA abs ASL abs --- BPL rel ORA ind,Y --- --- --- ORA zpg,X ASL zpg,X --- CLC impl ORA abs,Y --- --- --- ORA abs,X ASL abs,X --- JSR abs AND X,ind --- --- BIT zpg AND zpg ROL zpg --- PLP impl AND # ROL A --- BIT abs AND abs ROL abs --- BMI rel AND ind,Y --- --- --- AND zpg,X ROL zpg,X --- SEC impl AND abs,Y --- --- --- AND abs,X ROL abs,X --- RTI impl EOR X,ind --- --- --- EOR zpg LSR zpg --- PHA impl EOR # LSR A --- JMP abs EOR abs LSR abs --- BVC rel EOR ind,Y --- --- --- EOR zpg,X LSR zpg,X --- CLI impl EOR abs,Y --- --- --- EOR abs,X LSR abs,X --- RTS impl ADC X,ind --- --- --- ADC zpg ROR zpg --- PLA impl ADC # ROR A --- JMP ind ADC abs ROR abs --- BVS rel ADC ind,Y --- --- --- ADC zpg,X ROR zpg,X --- SEI impl ADC abs,Y --- --- --- ADC abs,X ROR abs,X --- --- STA X,ind --- --- STY zpg STA zpg STX zpg --- DEY impl --- TXA impl --- STY abs STA abs STX abs --- BCC rel STA ind,Y --- --- STY zpg,X STA zpg,X STX zpg,Y --- TYA impl STA abs,Y TXS impl --- --- STA abs,X --- --- LDY # LDA X,ind LDX # --- LDY zpg LDA zpg LDX zpg --- TAY impl LDA # TAX impl --- LDY abs LDA abs LDX abs --- BCS rel LDA ind,Y --- --- LDY zpg,X LDA zpg,X LDX zpg,Y --- CLV impl LDA abs,Y TSX impl --- LDY abs,X LDA abs,X LDX abs,Y --- CPY # CMP X,ind --- --- CPY zpg CMP zpg DEC zpg --- INY impl CMP # DEX impl --- CPY abs CMP abs DEC abs --- BNE rel CMP ind,Y --- --- --- CMP zpg,X DEC zpg,X --- CLD impl CMP abs,Y --- --- --- CMP abs,X DEC abs,X --- CPX # SBC X,ind --- --- CPX zpg SBC zpg INC zpg --- INX impl SBC # NOP impl --- CPX abs SBC abs INC abs --- BEQ rel SBC ind,Y --- --- --- SBC zpg,X INC zpg,X --- SED impl SBC abs,Y --- --- --- SBC abs,X INC abs,X ---
"""

b="BRK impl --- ORA zpg "

currentAdress=0
state="FINDOPCODE"
opcode=""
type=""

output=""

def store():
    line="(\""
    line+=opcode
    line+="\",\""
    if type=="impl" or type=="A":
        line+="NONE"
    if type=="zpg":
        line+="ZP"
    if type=="#":
        line+="IMM"
    if type=="X,ind":
        line+="INDEXINDX"
    if type=="ind,Y":
        line+="INDEXINDY"
    if type=="abs,X":
        line+="INDEXX"
    if type=="abs,Y":
        line+="INDEXY"
    if type=="rel":
        line+="RELTOKEN"
    if type=="abs":
        line+="DIR"
    if type=="ind":
        line+="IND"
    if type=="zpg,X":
        line+="ZPX"
    if type=="zpg,Y":
        line+="ZPY"

    line+="\"): "
    line+=hex(currentAdress)
    line+=","

    #output+=line
    print(line)
    #print(currentAdress)
    #print(opcode)
    #print(type)



for char in a:
    if char.isupper() and state=="FINDOPCODE":
        state="FINISHOPCODE"
        opcode+=char
    elif char.isupper() and state=="FINISHOPCODE":
        opcode+=char
    elif char=="-":
        state="INVALIDOPCODE"
    elif char==" " or char ==" ":
        if state=="FINISHOPCODE":
            state="FINDTYPE"
        elif state=="FINDTYPE":
            state="FINDOPCODE"
            store()
            currentAdress+=1
            opcode=""
            type=""
        elif state=="INVALIDOPCODE":
            state="FINDOPCODE"
            currentAdress+=1
            opcode=""
            type=""
    else:#char is lowercase letter or punctuation
        if state=="FINDTYPE":
            type+=char
