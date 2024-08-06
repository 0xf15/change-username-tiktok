# coding:utf-8
import hashlib
import json
from time import time
from hashlib import md5
from copy import deepcopy
from random import choice


def file_data(path):
    with open(path, 'rb') as f:
        result = f.read()
    return result


def hex_string(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string


def reverse(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return int(tmp_string[1:] + tmp_string[:1], 16)


def RBIT(num):
    result = ''
    tmp_string = bin(num)[2:]
    while len(tmp_string) < 8:
        tmp_string = '0' + tmp_string
    for i in range(0, 8):
        result = result + tmp_string[7 - i]
    return int(result, 2)


class XG:
    def __init__(self, debug):
        self.length = 0x14
        self.debug = debug
        self.hex_CE0 = [0x05, 0x00, 0x50, choice(range(0, 0xFF)), 0x47, 0x1e, 0x00, 8 * choice(range(0, 0x1F))]

    def addr_BA8(self):
        tmp = ''
        hex_BA8 = []
        for i in range(0x0, 0x100):
            hex_BA8.append(i)
        for i in range(0, 0x100):
            if i == 0:
                A = 0
            elif tmp:
                A = tmp
            else:
                A = hex_BA8[i - 1]
            B = self.hex_CE0[i % 0x8]
            if A == 0x05:
                if i != 1:
                    if tmp != 0x05:
                        A = 0
            C = A + i + B
            while C >= 0x100:
                C = C - 0x100
            if C < i:
                tmp = C
            else:
                tmp = ''
            D = hex_BA8[C]
            hex_BA8[i] = D
        return hex_BA8

    def initial(self, debug, hex_BA8):
        tmp_add = []
        tmp_hex = deepcopy(hex_BA8)
        for i in range(self.length):
            A = debug[i]
            if not tmp_add:
                B = 0
            else:
                B = tmp_add[-1]
            C = hex_BA8[i + 1] + B
            while C >= 0x100:
                C = C - 0x100
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            while E >= 0x100:
                E = E - 0x100
            F = tmp_hex[E]
            G = A ^ F
            debug[i] = G
        return debug

    def calculate(self, debug):
        for i in range(self.length):
            A = debug[i]
            B = reverse(A)
            C = debug[(i + 1) % self.length]
            D = B ^ C
            E = RBIT(D)
            F = E ^ self.length
            G = ~F
            while G < 0:
                G += 0x100000000
            H = int(hex(G)[-2:], 16)
            debug[i] = H
        return debug

    def main(self):
        result = ''
        for item in self.calculate(self.initial(self.debug, self.addr_BA8())):
            result = result + hex_string(item)

        return '8402{}{}{}{}{}'.format(hex_string(self.hex_CE0[7]), hex_string(self.hex_CE0[3]),
                                       hex_string(self.hex_CE0[1]), hex_string(self.hex_CE0[6]), result)


def getxg(param="", stub="", cookie=""):
    gorgon = []
    ttime = time()

    url_md5 = md5(bytearray(param, 'utf-8')).hexdigest()
    for i in range(0, 4):
        gorgon.append(int(url_md5[2 * i: 2 * i + 2], 16))

    if stub:
        for i in range(0, 4):
            gorgon.append(int(stub[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)

    if cookie:
        cookie_md5 = md5(bytearray(cookie, 'utf-8')).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(cookie_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)

    gorgon = gorgon + [0x0, 0x8, 0x10, 0x9]

    Khronos = hex(int(ttime))[2:]
    for i in range(0, 4):
        gorgon.append(int(Khronos[2 * i: 2 * i + 2], 16))

    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}


def get_stub(data):
    if isinstance(data, dict):
        data = json.dumps(data)

    if isinstance(data, str):
        data = data.encode(encoding='utf-8')
    if data == None or data == "" or len(data) == 0:
        return "00000000000000000000000000000000"

    m = hashlib.md5()
    m.update(data)
    res = m.hexdigest()
    res = res.upper()
    return res
