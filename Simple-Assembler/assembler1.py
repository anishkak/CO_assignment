opDict = {'add': ['00000', 'A'], 'sub': ['00001', 'A'], 'mov_imm': ['00010', 'B'], 'mov_reg': ['00011', 'C'],
          'ld': ['00100', 'D'], 'st': ['00101', 'D'], 'mul': ['00110', 'A'], 'div': ['00111', 'C'],
          'rs': ['01000', 'B'], 'ls': ['01001', 'B'], 'xor': ['01010', 'A'], 'or': ['01011', 'A'],
          'and': ['01100', 'A'], 'not': ['01101', 'C'], 'cmp': ['01110', 'C'], 'jmp': ['01111', 'E'],
          'jlt': ['10000', 'E'], 'jgt': ['10001', 'E'], 'je': ['10010', 'E'], 'hlt': ['10011', 'F']}

inst_list = ['add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp',
             'jmp', 'jlt', 'jgt', 'je', 'hlt']

regAdd = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110',
          'FLAGS': '111'}


def main():
    line_lst = []
    var_lst = []
    lbl_lst = []
    typeA_list = ['add', 'sub', 'mul', 'xor', 'or', 'and']
    typeB_list = ['ls', 'rs']
    typeC_list = ['div', 'not', 'cmp']
    typeD_list = ['ld', 'st']
    typeE_list = ['jmp', 'je', 'jgt', 'jlt']
    typeF_list = ['hlt']
    typeM_list = ['mov']
    i = 0
    flag = 0
    while True:
        try:
            line = input()
            i += 1
            line = line.strip()
            if line == "":
                continue
            line_lst.append(line+" "+str(i))

        except EOFError:
            break

    for j in line_lst:
        j = j.strip()
        chk = j.split()
        for k in chk:
            if ':' in k:
                lbl_lst.append(k)


    for i in line_lst:
        i = i.strip()
        line = i.split()

 
        if line[0] not in inst_list:
            if 'var' not in line[0] and ':' not in line[0]:
                print("Syntax Error in line " + line[-1])
                exit()

        if line[0] == 'var':
            if flag==0:
                var_lst.append(line[1])
            else:
                print("error at line "+ line[-1]+": variable should be defined at beginning")
                exit()

        for element in typeA_list:
            if element in line:
                index_add = line.index(element)
                inst = line[index_add]
                list_add = []

                for i in range(1, 4):
                    if line[index_add + i] in regAdd.keys():
                        if line[index_add + i] == 'FLAGS':
                            print("Error at line " + line[-1]+": Illegal use of FLAGS")
                            exit()
                        list_add.append(line[index_add + i])

                    else:
                        print("Error at line " + line[-1]+": Register not found")
                        exit()
                if len(list_add) == 3:
                    reg1 = list_add[0]
                    reg2 = list_add[1]
                    reg3 = list_add[2]
                else:
                    print("Error at line" + line[-1] + ": Invalid syntax")
                    exit()

                if line[index_add+4] != line[-1]:
                    print('General Syntax Error at line ' + line[-1])
                    exit()
                typeA(inst, reg1, reg2, reg3)
                flag=1

        for element in typeB_list:
            if element in line:
                index_add = line.index(element)
                inst = line[index_add]

                if line[index_add + 1] in regAdd:
                    if line[index_add + 1] == 'FLAGS':
                        print("Error at line " + line[-1] + ": Illegal use of FLAGS")
                        exit()
                    reg1 = line[index_add+1]
                else:
                    print("Error at line " + line[-1]+": Register not found")
                    exit()
                if '$' in line[index_add + 2]:
                    num = line[index_add + 2]
                    imm = int(num.replace('$', ''))
                    if imm < 0 or imm > 255:
                        print("Error at line " + line[-1]+": Immediate value out of range")
                        exit()
                else:
                    print("Error at line" + line[-1] + ": Invalid syntax")
                    exit()

                if line[index_add+3] != line[-1]:
                    print('General Syntax Error at line ' + line[-1])
                    exit()
                typeB(inst, reg1, imm)
                flag=1

        for element in typeC_list:
            if element in line:
                index_add = line.index(element)
                inst = line[index_add]
                list_add = []

                for i in range(1, 3):
                    if line[index_add + i] in regAdd.keys():
                        if line[index_add + i] == 'FLAGS':
                            print("Error at line " + line[-1]+": Illegal use of FLAGS")
                            exit()
                        list_add.append(line[index_add + i])
                    else:
                        print("Error at line " + line[-1]+": register not found")
                        exit()
                if len(list_add) == 2:
                    reg1 = list_add[0]
                    reg2 = list_add[1]
                else:
                    print("Error at line" + line[-1] + ": invalid syntax")
                    exit()

                if line[index_add+3] != line[-1]:
                    print('General Syntax Error at line ' + line[-1])
                    exit()

                typeC(inst, reg1, reg2)
                flag=1

        for element in typeD_list:
            if element in line:
                index_add = line.index(element)
                inst = line[index_add]

                if line[index_add + 1] in regAdd:
                    if line[index_add + 1] == 'FLAGS':
                        print("Error at line " + line[-1] + ": Illegal use of FLAGS")
                        exit()
                    reg1 = line[1]
                else:
                    print("Error at line " + line[-1]+": register not found")
                    exit()
                var = line[index_add + 2]
                if var in lbl_lst:
                    print('Error at line ' + line[-1] + ' :Misuse of label')
                    exit()
                if var not in var_lst:
                    print('Error at line ' + line[-1] + ' :Undefined Variable')
                    exit()
                if line[index_add+3] != line[-1]:
                    print('General Syntax Error at line ' + line[-1])
                    exit()
                for k in var_lst:
                    if k == var:
                        typeD(inst, reg1, getVar(line_lst, var))
                        flag=1

        for element in typeE_list:
            if element in line:
                index_add = line.index(element)
                inst = line[index_add]
                lab = line[index_add + 1] + ':'
                if lab in var_lst:
                    print('Error at line ' + line[-1] + ' : Misuse of variable')
                    exit()
                if lab not in lbl_lst:
                    print('Error at line ' + line[-1] + ' : Undefined Label')
                    exit()
                if line[index_add+2] != line[-1]:
                    print('General Syntax Error at line ' + line[-1])
                    exit()
                for k in line_lst:
                    if lab in k:
                        typeE(inst, getLbl(line_lst, k))
                        flag=1


        for element in typeF_list:
            if element in line:
                index_add = line.index(element)
                if line[index_add+1] != line[-1]:
                    print('General Syntax Error at line ' + line[-1])
                    exit()
                inst = line[index_add]
                if ":" in line[0]:
                    typeF(inst)
                    flag=1
                else:
                    if int(line[-1]) == len(line_lst):
                        typeF(inst)
                        exit()
                    else:
                        print("Error: hlt not being used as the last instruction")
                        exit()


        for element in typeM_list:
            if element in line:
                index_add = line.index(element)

                if line[index_add + 1] in regAdd:
                    if line[index_add+1] != 'FLAGS':
                        reg1 = line[index_add+1]
                    else:
                        print("Error at line " + line[-1]+": Illegal use of FLAGS")
                        exit()
                else:
                    print("Error at line " + line[-1]+": Register not found")
                    exit()

                if '$' in line[index_add + 2]:
                    inst = 'mov_imm'
                    num = line[index_add + 2]
                    imm = int(num.replace('$', ''))
                    if line[index_add + 3] != line[-1]:
                        print('General Syntax Error at line ' + line[-1])
                        exit()
                    if imm < 0 or imm > 255:
                        print("Error at line " + line[-1]+": Immediate value out of range")
                        exit()
                    typeB(inst, reg1, imm)
                    flag=1
                elif line[index_add + 2] in regAdd:
                    inst = 'mov_reg'
                    reg2 = line[index_add+2]
                    if line[index_add + 3] != line[-1]:
                        print('General Syntax Error at line ' + line[-1])
                        exit()
                    typeC(inst, reg1, reg2)
                    flag=1
                else:
                    print("Error at line" + line[-1] + ": Invalid syntax")
                    exit()

        for k in line:
            if ':' in k:
                for element in opDict.keys():
                    if element + ":" == k:
                        print("Error: Cannot use instructions as label names")
                        exit()

                lbl_lst.append(k)
                flag=1

        if 'hlt' not in line_lst[-1]:
            print("Error: hlt not being used as the last instruction")
            exit()


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
    lst = []
    for k in a:
        if 'var' not in k:
            lst.append(k)
    for i in lst:
        if ':' in i:
            lblDict[i] = lst.index(i)
    return lblDict[lb]


if __name__ == "__main__":
    main()