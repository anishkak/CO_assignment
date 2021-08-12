from sys import *

opDict = {'add': ['00000', 'A'], 'sub': ['00001', 'A'], 'mov_imm': ['00010', 'B'], 'mov_reg': ['00011', 'C'],
          'ld': ['00100', 'D'], 'st': ['00101', 'D'], 'mul': ['00110', 'A'], 'div': ['00111', 'C'],
          'rs': ['01000', 'B'], 'ls': ['01001', 'B'], 'xor': ['01010', 'A'], 'or': ['01011', 'A'],
          'and': ['01100', 'A'], 'not': ['01101', 'C'], 'cmp': ['01110', 'C'], 'jmp': ['01111', 'E'],
          'jlt': ['10000', 'E'], 'jgt': ['10001', 'E'], 'je': ['10010', 'E'], 'hlt': ['10011', 'F']}

regAdd = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110',
          'FLAGS': '111'}
imm = False
inst = ''
mem_add = ''
reg1 = ''
reg2 = ''
reg3 = ''
a=[]

def main():
    global imm
    global inst
    global mem_add
    global reg1
    global reg2
    global reg3 
    while True:
        try:

            line = input().strip()
            
            if line == "":
                continue
            a.append(line)

            #line = line.strip()
            #line = line.split("\n")
            
        except EOFError:
                break
    
    for i in a:
            line = i.split()
            if len(line)==0:
                exit()
            else:
                inst = line[0]

                if len(line) == 2:
                    mem_add = line[1]
                elif len(line) == 3:
                    reg1 = line[1]
                    if '$' in line[2]:
                        num = line[2]
                        imm = int(num.replace('$', ''))
                    elif line[2] in regAdd.keys():
                        reg2 = line[2]
                    else:
                        mem_add = int(line[2])
                elif len(line) == 4:
                    reg1 = line[1]
                    reg2 = line[2]
                    reg3 = line[3]

                if inst.lower() != 'mov':
                    if opDict[inst][1] == 'A':
                        typeA(inst, reg1, reg2, reg3)
                    if opDict[inst][1] == 'B':
                        typeB(inst, reg1, reg2, imm)
                    if opDict[inst][1] == 'C':
                        typeC(inst, reg1, reg2)
                    if opDict[inst][1] == 'D':
                        typeD(inst, reg1, mem_add)
                    if opDict[inst][1] == 'E':
                        typeE(inst, reg1, mem_add)
                    if opDict[inst][1] == 'F':
                        typeF(inst)

                if inst.lower() == 'mov':
                    if imm:
                        ist = 'mov_imm'
                        typeB(ist, reg1, imm)
                    elif reg2:
                        ist = 'mov_reg'
                        typeC(ist, reg1, reg2)

def typeA(inst, reg1, reg2, reg3):
    if inst in opDict.keys():
        if reg1 in regAdd.keys():
            if reg2 in regAdd.keys():
                if reg3 in regAdd.keys():
                    print(opDict[inst][0] + '00' + regAdd[reg1] + regAdd[reg2] + regAdd[reg3])


def typeB(inst, reg1, imm):
    if inst in opDict.keys():
        if reg1 in regAdd.keys():
            print(opDict[inst][0] + regAdd[reg1] + format(imm, '08b'))


def typeC(inst, reg1, reg2):
    if inst in opDict.keys():
        if reg1 in regAdd.keys():
            if reg2 in regAdd.keys():
                print(opDict[inst][0] + '00000' + regAdd[reg1] + regAdd[reg2])


def typeD(inst, reg1, mem_add):
    if inst in opDict.keys():
        if reg1 in regAdd.keys():
            print(opDict[inst][0] + regAdd[reg1] + format(mem_add, '08b'))


def typeE(inst, mem_add):
    if inst in opDict.keys():
        if reg1 in regAdd.keys():
            print(opDict[inst][0] + '000' + format(mem_add, '08b'))


def typeF(inst):
    if inst in opDict.keys():
        print(opDict[inst][0] + '00000000000')
        exit()


if __name__ == "__main__":
    main()