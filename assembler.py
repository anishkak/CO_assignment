opDict = {'add': ['00000', 'A'], 'sub': ['00001', 'A'], 'mov_imm': ['00010', 'B'], 'mov_reg': ['00011', 'C'],
          'ld': ['00100', 'D'], 'st': ['00101', 'D'], 'mul': ['00110', 'A'], 'div': ['00111', 'C'],
          'rs': ['01000', 'B'], 'ls': ['01001', 'B'], 'xor': ['01010', 'A'], 'or': ['01011', 'A'],
          'and': ['01100', 'A'], 'not': ['01101', 'C'], 'cmp': ['01110', 'C'], 'jmp': ['01111', 'E'],
          'jlt': ['10000', 'E'], 'jgt': ['10001', 'E'], 'je': ['10010', 'E'], 'hlt': ['10011', 'F']}

regAdd = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110',
          'FLAGS': '111'}


def main():
    line_lst = []
    var_lst = []
    lbl_lst = []
    while True:
        try:
            line = input()
            line = line.strip()
            if line == "":
                continue
            line_lst.append(line)
        except EOFError:
            break

    for i in line_lst:
        i = i.strip()
        line = i.split()


        if line[0] == 'add' or line[0] == 'sub' or line[0] == 'mul' or line[0] == 'xor' or line[0] == 'or' or line[0] == 'and':
            if len(line)>=4:
                inst = line[0]
                reg1 = line[1]
                reg2 = line[2]
                reg3 = line[3]
                typeA(inst, reg1, reg2, reg3)       
            else:
                print("error: incorrect instruction syntax")


        if line[0] == 'rs' or line[0] == 'ls':
            if len(line)>=3:
                inst = line[0]
                reg1 = line[1]
                if '$' in line[2]:
                    inst = line[0]
                    num = line[2]
                    imm = int(num.replace('$', ''))
                typeB(inst, reg1, imm)
            else:
                print("error: incorrect instruction syntax")


        if line[0] == 'div' or line[0] == 'not' or line[0] == 'cmp':
            
            inst = line[0]
            reg1 = line[1]
            reg2 = line[2]
            typeC(inst, reg1, reg2)


        if line[0] == 'ld' or line[0] == 'st':
            inst = line[0]
            reg1 = line[1]
            var = line[2]
            for k in var_lst:
                if k == var:
                    typeD(inst, reg1, getVar(line_lst, var))


        if line[0] == 'jmp' or line[0] == 'jlt' or line[0] == 'jgt' or line[0] == 'je':
            inst = line[0]
            lab = line[1] + ':'
            for k in lbl_lst:
                if lab == k:
                    typeE(inst, getLbl(line_lst, k))


        if line[0] == 'hlt':
            inst = line[0]
            typeF(inst)


        if line[0] == 'mov':
            reg1 = line[1]
            if '$' in line[2]:
                inst = 'mov_imm'
                num = line[2]
                imm = int(num.replace('$', ''))
                typeB(inst, reg1, imm)
            else:
                inst = 'mov_reg'
                reg2 = line[2]
                typeC(inst, reg1, reg2)

        if line[0] == 'var':
            var_lst.append(line[1])    #error check

        for k in line:
            if ':' in k:
                for element in opDict.keys():
                    if element+":" == k:
                        print("Error: cannot use instructions as label names")
                lbl_lst.append(k)


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
        print(opDict[inst][0] + '000' + format(mem_add, '08b'))


def typeF(inst):
    if inst in opDict.keys():
        print(opDict[inst][0] + '00000000000')
        exit()


def getVar(a, x):
    b = {}
    c = []
    d = []
    for i in a:
        if 'var' not in i:
            c.append(i)
        elif 'var' in i:
            d.append(i)

    n1 = len(a) - len(d)
    for j in d:
        e = j.split()
        b[e[1]] = n1
        n1 += 1
    return b[x]


def getLbl(a, lb):
    lblDict = {}
    for i in a:
        if ':' in i:
            lblDict[i] = a.index(i)
    return lblDict[lb]


if __name__ == "__main__":
    main()