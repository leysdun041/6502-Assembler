import assemble

memory=[]

memoryUsed=[]

#Token in location to be filled. Address of the instruction with token
tokenFill=[
#Format (address, token, relative)

]

#Token name and location. Token location
resolvedTokens=[
#Format (token, address)

]

def initmemory():
    for i in range((2**16)):
        memory.append(0x00)
        memoryUsed.append(False)

#Will not do little edian format
def addmemory(address, data):
    if data>=0x00 and data<=0xFF and address>=0x0000 and address<=0xFFFF:
        if memoryUsed[address]==True:
            assemble.error("ADRESS: "+hex(address)+" is duplicated",-1)
        memory[address]=data
        memoryUsed[address]=True
    elif data>=0xFF and data<=0xFFFF and address>=0x0000 and address<=0xFFFF:
        if memoryUsed[address]==True or memoryUsed[address+1]==True:
            assemble.error("ADRESS: "+hex(address)+" is duplicated",-1)
        memoryUsed[address]=True
        memoryUsed[address+1]=True
        memory[address+1]=(data&0xFF)
        memory[address]=(data&0xFF00)>>8

def addtoken(address, token, relative):
    if address>=0x0000 and address<=0xFFFF:
        tokenFill.append((address,token, relative))

def resolvetoken(token,address):
    resolvedTokens.append((token,address))


def resolvealltokens():
    for token in tokenFill:
        for resolvedToken in resolvedTokens:
            if token[1]==resolvedToken[0]:
                #token has been resolved
                if token[2]==False:
                    addmemory(token[0],resolvedToken[1])
                else:
                    difference=resolvedToken[1]-token[0]+1
                    if difference<0:
                        difference=~difference+1 #Twos complement negation
                    addmemory(token[0],difference)

def writememory(file):
    resolvealltokens()
    newFileByteArray = bytearray(memory)
    file.write(newFileByteArray)
