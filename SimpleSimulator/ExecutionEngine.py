opDict = {'add': '00000', 'sub': '00001', 'mov_imm': '00010', 'mov_reg': '00011',
          'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111',
          'rs': '01000', 'ls': '01001', 'xor': '01010', 'or': '01011',
          'and': '01100', 'not': '01101', 'cmp': '01110', 'jmp': '01111',
          'jlt': '10000', 'jgt': '10001', 'je': '10010', 'hlt': '10011'}

regDict = {'000': '0000000000000000', '001': '0000000000000000', '010': '0000000000000000', '011': '0000000000000000',
           '100': '0000000000000000', '101': '0000000000000000', '110': '0000000000000000', '111': '0000000000000000'}

memDict = {}

pc = 0


def main():
    global pc
    flag = 0
    line_list = []
    for i in range(257):
        line_list[i] = 0
    num = 0
    while num < 257:
        try:
            line = input()
            k = line + " " + str(num)
            line_list[num] = k
            num += 1

        except:
            pass

    for l in line_list:
        while flag == 0:
            if pc == l[-1]:
                if l[0:5] in ['00000', '00001', '00110', '01010', '01011', '01100']:
                    inst = l[0:5]
                    typeA(l, inst)
                    out()
                    pc = l[-1]
                if l[0:5] in ['01000', '01001', '00010']:
                    inst = l[0:5]
                    typeB(l, inst)
                    out()
                    pc = l[-1]
                if l[0:5] in ['00011', '00111', '01101', '01110']:
                    inst = l[0:5]
                    typeC(l, inst)
                    out()
                    pc = l[-1]
                if l[0:5] in ['00100', '00101']:
                    inst = l[0:5]
                    typeD(l, inst, line_list)
                    out()
                    pc = l[-1]
                if l[0:5] in ['01111', '10000', '10001', '10010']:
                    inst = l[0:5]
                    typeE(l, inst)
                    out()
                    pc = l[-1]
                if l[0:5] in ['10011']:
                    inst = l[0:5]
                    typeF(l, inst)
                    out()
                    pc = l[-1]

    print(line_list)


def typeA(l, inst):
    rd = l[7:10]
    op1 = l[10:13]
    op2 = l[13:16]
    reg1 = regDict[rd]
    reg2 = regDict[op1]
    reg3 = regDict[op2]
    if inst == '00000':
        x = int(reg2, 2) + int(reg3, 2)
        y = format(x, '016b')
    elif inst == '00001':
        x = int(reg2, 2) - int(reg3, 2)
        y = format(x, '016b')
    elif inst == '01100':
        x = int(reg2, 2) & int(reg3, 2)
        y = format(x, '016b')
    elif inst == '00110':
        x = int(reg2, 2) * int(reg3, 2)
        y = format(x, '016b')
    elif inst == '01010':
        x = int(reg2, 2) ^ int(reg3, 2)
        y = format(x, '016b')
    elif inst == '01011':
        x = int(reg2, 2) | int(reg3, 2)
        y = format(x, '016b')
    if x < 0 or x > 2 ** 16:
        regDict['111'] = '0000000000001000'
        regDict[rd] = y[-16:]
    else:
        regDict['111'] = '0000000000000000'
        regDict[rd] = y


def typeB(l, inst):
    rd = l[5:8]
    imm = l[8:16]
    reg1 = regDict[rd]
    if inst == '00010':
        x = format(int(imm, 2), '016b')
    elif inst == '01000':
        x = int(reg1, 2) >> int(imm, 2)
    elif inst == '01001':
        x = int(reg1, 2) >> int(imm, 2)
    regDict[rd] = x


def typeC(l, inst):
    op1 = l[10:13]
    op2 = l[13:16]
    reg1 = regDict[op1]
    reg2 = regDict[op2]
    if inst == '00011':
        regDict[op1] = reg2
    elif inst == '00111':
        regDict['000'] = format(int(reg1, 2) // int(reg2, 2), '016b')
        regDict['001'] = format(int(reg1, 2) % int(reg2, 2), '016b')
    elif inst == '01101':
        regDict[reg1] = ''.join(['1' if i == '0' else '0' for i in reg2])
    elif inst == '01110':
        ele1 = int(reg1, 2)
        ele2 = int(reg2, 2)
        if ele1 == ele2:
            regDict['111'] = '0000000000000001'
        elif ele1 > ele2:
            regDict['111'] = '0000000000000010'
        elif ele1 < ele2:
            regDict['111'] = '0000000000000100'


def typeD(l, inst, line_list):
    rd = l[5:8]
    mem_add = l[8:16]
    adr = int(mem_add, 2)
    if inst == '00101':  # st
        for i in line_list:
            if i == adr:
                line_list[i] = regDict[rd]
    elif inst == '00100':  # ld
        for i in line_list:
            if i == adr:
                val = line_list[i]
        regDict[rd] = val


def typeE(l, inst):
    global pc
    mem_add = l[8:16]
    adr = int(mem_add, 2)
    if inst == '01111':  # uncon
        pc = adr
    if inst == '10010':  # eq
        if regDict['111'] == '0000000000000001':
            pc = adr
    if inst == '10000':  # less
        if regDict['111'] == '0000000000000100':
            pc = adr
    if inst == '10001':  # greater
        if regDict['111'] == '0000000000000010':
            pc = adr


def typeF(l, inst):
    flag = 1


def out():
    print_pc = format(pc, '08b')
    res_str = ''
    for i in regDict.values():
        res_str = res_str + i + ' '
    print(print_pc + ' ' + res_str)


if __name__ == "__main__":
    main()