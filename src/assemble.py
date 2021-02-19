import sys
#other file
import decode
import instructions
import build

def getLines(file):
    linelist=[]
    text=file.read()
    curstring=""
    for char in text:
        if char=="\n":
            linelist.append(curstring)
            curstring=""
        else:
            curstring+=char
    return linelist

def linelisttoclass(linelist):
    classlist=[]
    line=1
    for curline in linelist:
        tmp=decode.line(curline,line)
        #BE sure to strip all comments
        if tmp.type!="COMMENT":
            classlist.append(tmp)
        line+=1
    return classlist

def createbuild(classList):
    build.initmemory()
    currentAdress=0
    for line in classList:
        print("NEWLINE")
        print(line.text)

        if line.type=="DIR" and line.dir=="ORG":
            currentAdress=line.dirarg
        if line.type=="TOKEN":
            print(line.token)
            build.resolvetoken(line.token, currentAdress)
        if line.type=="CODE":
            print(line.instruction)
            a=line.decodeinstruction()
            for i in range(len(a)):
                if type(a[i]) is int:
                    a[i]=hex(a[i])
            print(a)
            instr=line.decodeinstruction()
            build.addmemory(currentAdress, instr[0])
            currentAdress+=1
            if line.operandtoken==False and line.codetype!="NONE":
                build.addmemory(currentAdress, instr[1])
                build.addmemory(currentAdress+1, instr[2])
                currentAdress+=2
            elif line.codetype!="NONE":
                if line.codetype=="RELTOKEN":
                    build.addtoken(currentAdress, instr[1],True)
                    currentAdress+=1
                else:
                    build.addtoken(currentAdress, instr[1],False)
                    currentAdress+=2



def error(reason,line):
    print("ERROR")
    print("Line: "+str(line))
    print(reason)
    sys.exit()

def main():
    filename=sys.argv[1]
    file=open(filename,"r")

    lines=getLines(file)
    lineclass=linelisttoclass(lines)

    createbuild(lineclass)
    build.writememory(open("a.out","wb"))



if __name__ == "__main__":
    main()
