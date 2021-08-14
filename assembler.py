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
    typeA_list=['add','sub','mul','xor','or','and']
    typeB_list=['ls','rs']
    typeC_list=['div','not','cmp']
    typeD_list=['ld','st']
    typeE_list=['jmp','je','jgt','jlt']
    typeF_list=['hlt']
    while True:
        try:
            line = input()
            line = line.strip()
            if line == "":
                break
            line_lst.append(line)
            j = line.strip()
            line = j.split()
            for k in line:
                if ':' in k:
                    for element in opDict.keys():
                        if element+":" == k:
                            print("Error: cannot use instructions as label names")
                            exit()
                    lbl_lst.append(k)
        except EOFError:
            break
    print(lbl_lst)
    for i in line_lst:
        i = i.strip()
        line = i.split()


        for element in typeA_list:
            if element in line:
                index_add=line.index(element)
                inst = line[index_add]
                list_add=[]
                for i in range(1,4):
                    if line[index_add+i] in regAdd.keys():
                        list_add.append(line[index_add+i])
                    else:
                        print("Error: register not found")
                        exit()
                if len(list_add)==3:
                    reg1=list_add[0]
                    reg2=list_add[1]
                    reg3=list_add[2]
                else:
                    print("invalid syntax")
                    exit()
                
                typeA(inst, reg1, reg2, reg3)       
 
        for element in typeB_list:
            if element in line:
                index_add=line.index(element)
                inst = line[index_add]
                if line[index_add+1] in regAdd:
                    reg1 = line[1]
                else:
                    print("Error: register not found")
                    exit()
                if '$' in line[index_add+2]:
                    num = line[index_add+2]
                    imm = int(num.replace('$', ''))
                else:
                    print("Error: invalid syntax")
                    exit()
                typeB(inst, reg1, imm)
            


        for element in typeC_list:
            if element in line:
                index_add=line.index(element)
                inst = line[index_add]
                list_add=[]
                for i in range(1,3):
                    if line[index_add+i] in regAdd.keys():
                        list_add.append(line[index_add+i])
                    else:
                        print("Error: register not found")
                        exit()
                if len(list_add)==2:
                    reg1=list_add[0]
                    reg2=list_add[1]
                else:
                    print("invalid syntax")
                    exit()
                
                typeC(inst, reg1, reg2)


        for element in typeD_list:
            if element in line:
                index_add=line.index(element)
                inst = line[index_add]
                if line[index_add+1] in regAdd:
                    reg1 = line[1]
                else:
                    print("Error: register not found")
                    exit()
                var = line[index_add+2]
                for k in var_lst:
                    if k == var:
                        typeD(inst, reg1, getVar(line_lst, var))


        for element in typeE_list:
            if element in line:
                index_add=line.index(element)
                inst = line[index_add]
                lab = line[index_add+1] + ':'
                for k in lbl_lst:
                    if lab == k:
                        print(line)
                        print(line_lst)
                        typeE(inst, getLbl(line_lst, lab))



        for element in typeF_list:
            if element in line:
                index_add=line.index(element)
                inst = line[index_add]
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
                            exit()
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
        i=i.strip()
        i=i.split()
        if ':' in i:
            lblDict[i] = a.index(i)
    print(lblDict)
    return lblDict[lb]



if __name__ == "__main__":
    main()