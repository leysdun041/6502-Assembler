import instructions
import assemble

def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`,
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


class line:
    line=0
    text=""
    type=""

    dir=""
    dirarg=""

    token=""
    length=0


    instruction=""
    instructionhex=""
    codetype=""  #IMM, DIR, IND, INDEXY,INDEXX, INDEXINDX,INDEXINDY, TOKEN, RELTOKEN
    operand=""
    operandtoken=False

    def __init__(self,text,line):
        if len(text)==0:
            self.type="COMMENT"
            text=";"
        self.line=line
        self.text=text
        if text[0]==".":
            self.type="DIR"
            self.initdir()
        elif text[0]==";":
            self.type="COMMENT"
        else:
            if text[len(text)-1]==":":
                self.type="TOKEN"
                self.inittoken()
            else:
                self.type="CODE"
                self.initcode()

    def initdir(self):
        arg=False
        for char in self.text:
            if char==" ":
                arg=True
            elif arg==True:
                self.dirarg+=char
            elif arg==False:
                self.dir+=char
        self.dir=self.dir[-1:]
        if self.dirarg!="" and is_number(self.dirarg):
            self.dirarg=self.converttohex(self.dirarg)


    def inittoken(self):
        self.token=self.text[:-1]

    def initcode(self):
        instfound=False
        self.codetype="NONE"
        i=0
        for char in self.text:
            if char==" ":
                instfound=True
                char=self.text[i+1]
                if char=="#": #immediate
                    self.codetype="IMM"
                elif char=="(": #indirect
                    self.codetype="IND"
                    if is_number(self.text[i+2]) or self.text[i+2]=="$" or self.text[i+2]=="%":
                        self.operandtoken=False
                    else:
                        self.operandtoken=True #token indirect
                elif is_number(char) or char=="$" or char=="%": #direct
                    self.codetype="DIR"
                else: #token direct
                    self.codetype="DIR"
                    self.operandtoken=True
                self.parseoperand(i)
            elif instfound==False:
                self.instruction+=char
            i+=1

    def parseoperand(self,num):
        if self.codetype!="DIR" and self.operandtoken==False:
            text=self.text[num+2:]
        else:
            text=self.text[num+1:]
        end=False
        i=0
        for char in text:
            if char==")":
                pass
            elif char==",":
                if text[i+1]=="y":
                    if self.codetype=='DIR':
                        self.codetype='INDEXY'
                    if self.codetype=='IND':
                        self.codetype='INDEXINDY'
                if text[i+1]=="x":
                    if self.codetype=='DIR':
                        self.codetype='INDEXX'
                    if self.codetype=='IND':
                        self.codetype='INDEXINDX'
                end=True
            elif end==False:
                self.operand+=char
            i+=1
        if self.instruction in instructions.relInstruction:
            if self.operandtoken==True:
                self.codetype="RELTOKEN"
            else:
                assemble.error("RELATIVE instructions must have a token.",self.line)
        if self.operandtoken==False:
            self.operand=self.converttohex(self.operand)
        self.resolvelength()

    def converttohex(self,a):
        if a[0]=='$':
            a = int(a[1:], 16)
        elif a[0]=="%":
            a = int(a[1:], 2)
        elif is_number(a[0]):
            a=int(a,10)
        else:
            assemble.error("Unknown: "+a[0],self.line)
        return a

    def resolvelength(self):
        #IMM, DIR, IND, INDEXY,INDEXX, INDEXINDX,INDEXINDY, TOKEN, RELTOKEN, ZP, ZPX,ZPY, NONE

        if self.codetype in ("NONE"):
            self.length=1
        elif self.codetype in ("RELTOKEN","IMM","INDEXINDX","INDEXINDY","ZP","ZPX","ZPY"):
            self.length=2
        elif self.codetype in ("IND","TOKEN","DIR","INDEXY","INDEXX"):
            self.length=3

    def createOperand(self,returninstr):
        returninstr.append(self.operand&0xFF)
        returninstr.append((self.operand&0xFF00)>>8)
        if self.operand>0xFFFF:
            assemble.error("Operand is bigger than allowed",self.line)
        return returninstr

    def decodeinstruction(self):
        returninstr=[]
        for inst in instructions.instructionArray:
            if inst[0]==self.instruction and inst[1]==self.codetype:
                self.instructionhex=instructions.instructionArray[inst]
                returninstr.append(self.instructionhex)

                if self.operandtoken==False and self.operand!="":
                    self.createOperand(returninstr)
                elif self.operand!="":
                    returninstr.append(self.operand)
                return returninstr

        assemble.error("INSTRUCTION: "+self.instruction+" not found",self.line)
