import matplotlib.pyplot as plt
import numpy as np

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
    traces = []
    global pc
    pd = 0
    flag = 0
    cycle = 0
    line_list = []
    for i in range(256):
        line_list.append(format(0, '016b'))
    num = 0
    while num < 256:
        try:
            line = input()
            if line == "":
                break
            k = line + " " + str(num)
            line_list[num] = k
            num += 1

        except EOFError:
            break

    for l in line_list:
        l = l.strip()
        l = l.split()
        if pc == int(l[-1]):
            traces.append([cycle, pc])
            if l[0][0:5] == '00000' or l[0][0:5] == '00001' or l[0][0:5] == '00110' or l[0][0:5] == '01010' or l[0][0:5] == '01011' or l[0][0:5] == '01100':
                inst = l[0][0:5]
                typeA(l, inst)
                out(pc)
                pc += 1
            if l[0][0:5] == '01000' or l[0][0:5] == '01001' or l[0][0:5] == '00010':
                inst = l[0][0:5]
                typeB(l, inst)
                out(pc)
                pc += 1
            if l[0][0:5] == '00011' or l[0][0:5] == '00111' or l[0][0:5] == '01101' or l[0][0:5] == '01110':
                inst = l[0][0:5]
                typeC(l, inst)
                out(pc)
                pc += 1
            if l[0][0:5] == '00100' or l[0][0:5] == '00101':
                inst = l[0][0:5]
                typeD(l, inst, line_list, traces, cycle)
                out(pc)
                pc += 1
            if l[0][0:5] == '01111' or l[0][0:5] == '10000' or l[0][0:5] == '10001' or l[0][0:5] == '10010':
                inst = l[0][0:5]
                #out(pc)
                pd = pc
                typeE(l, inst)
                out(pd)
            if l[0][0:5] == '10011':
                inst = l[0][0:5]
                typeF(l, inst)
                out(pc)
                pc += 1
            cycle += 1

    mem_dump(line_list)
    cycle_list = []
    pc_list = []

    for i in traces:
        cycle_list.append(i[0])
        pc_list.append(i[1])
    plt.scatter(cycle_list, pc_list)
    plt.show()

    exit()


def mem_dump(line_list):
    for i in line_list:
        print(i[:17])


def typeA(l, inst):
    rd = l[0][7:10]
    op1 = l[0][10:13]
    op2 = l[0][13:16]
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
    if x > 2 ** 16:
        regDict['111'] = '0000000000001000'
        regDict[rd] = y[-16:]
    elif x < 0:
        regDict['111'] = '0000000000001000'
        regDict[rd] = '0000000000000000'
    else:
        regDict['111'] = '0000000000000000'
        regDict[rd] = y


def typeB(l, inst):
    rd = l[0][5:8]
    imm = l[0][8:16]
    reg1 = regDict[rd]
    if inst == '00010':
        x = format(int(imm, 2), '016b')
    elif inst == '01000':
        y = int(reg1, 2) >> int(imm, 2)
        x = format(y, '016b')
    elif inst == '01001':
        y = int(reg1, 2) << int(imm, 2)
        x = format(y, '016b')
    regDict[rd] = x
    regDict['111'] = '0000000000000000'


def typeC(l, inst):
    op1 = l[0][10:13]
    op2 = l[0][13:16]
    reg1 = regDict[op1]
    reg2 = regDict[op2]
    if inst == '00011':
        regDict[op1] = reg2
        regDict['111'] = '0000000000000000'
    elif inst == '00111':
        regDict['000'] = format(int(reg1, 2) // int(reg2, 2), '016b')
        regDict['001'] = format(int(reg1, 2) % int(reg2, 2), '016b')
        regDict['111'] = '0000000000000000'
    elif inst == '01101':
        regDict[op1] = ''.join(['1' if i == '0' else '0' for i in reg2])
        regDict['111'] = '0000000000000000'
    elif inst == '01110':
        ele1 = int(reg1, 2)
        ele2 = int(reg2, 2)
        if ele1 == ele2:
            regDict['111'] = '0000000000000001'
        elif ele1 > ele2:
            regDict['111'] = '0000000000000010'
        elif ele1 < ele2:
            regDict['111'] = '0000000000000100'


def typeD(l, inst, line_list, traces, cycle):
    rd = l[0][5:8]
    mem_add = l[0][8:16]
    adr = int(mem_add, 2)
    if inst == '00101':  # st
        line_list[adr]=regDict[rd]

    elif inst == '00100':  # ld
        regDict[rd]=line_list[adr]
    
    regDict['111'] = '0000000000000000'
    traces.append([cycle, adr])


def typeE(l, inst):
    global pc
    mem_add = l[0][8:16]
    adr = int(mem_add, 2)
    if inst == '01111':  # uncon
        pc = adr
    if inst == '10010':  # eq
        if regDict['111'] == '0000000000000001':
            pc = adr
        else:
            pc += 1
    if inst == '10000':  # less
        if regDict['111'] == '0000000000000100':
            pc = adr
        else:
            pc += 1
    if inst == '10001':  # greater
        if regDict['111'] == '0000000000000010':
            pc = adr
        else:
            pc += 1
    regDict['111'] = '0000000000000000'


def typeF(l, inst):
    flag = 1
    regDict['111'] = '0000000000000000'


def out(pc):
    print_pc = format(pc, '08b')
    res_str = ''
    for i in regDict.values():
        res_str = res_str + i + ' '
    print(print_pc + ' ' + res_str)


if __name__ == "__main__":
    main()