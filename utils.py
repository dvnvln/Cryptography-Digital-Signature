def translate(message):
    charcodes = [ord(c) for c in message]
    bytes = []
    for char in charcodes:
        bytes.append(bin(char)[2:].zfill(8))
    bits = []
    for byte in bytes:
        for bit in byte:
            bits.append(int(bit))
    return bits


def chunker(bits, chunk_length=8):
    chunked = []
    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b:b+chunk_length])
    return chunked

def fillZeros(bits, length=8, endian='LE'):
    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else: 
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits

def preprocessMessage(message):
    bits = translate(message)
    length = len(bits)
    message_len = [int(b) for b in bin(length)[2:].zfill(64)]
    if length < 448:
        bits.append(1)
        bits = fillZeros(bits, 448, 'LE')
        bits = bits + message_len
        return [bits]
    elif length == 448:
        bits.append(1)
        bits = fillZeros(bits, 1024, 'LE')
        bits[-64:] = message_len
        return chunker(bits, 512)
    else:
        bits.append(1)
        while len(bits) % 512 != 0:
            bits.append(0)
        bits[-64:] = message_len
    return chunker(bits, 512)


def initializer(values):
    binaries = [bin(int(v, 16))[2:] for v in values]
    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fillZeros(word, 32, 'BE'))
    return words

def b2Tob16(value):
    value = ''.join([str(x) for x in value])
    binaries = []
    for d in range(0, len(value), 4):
        binaries.append('0b' + value[d:d+4])
    hexes = ''
    for b in binaries:
        hexes += hex(int(b ,2))[2:]
    return hexes

def isTrue(x): return x == 1

def if_(i, y, z): return y if isTrue(i) else z

def and_(i, j): return if_(i, j, 0)
def AND(i, j): return [and_(ia, ja) for ia, ja in zip(i,j)] 

def not_(i): return if_(i, 0, 1)
def NOT(i): return [not_(x) for x in i]

def xor(i, j): return if_(i, not_(j), j)
def XOR(i, j): return [xor(ia, ja) for ia, ja in zip(i, j)]

def xorxor(i, j, l): return xor(i, xor(j, l))
def XORXOR(i, j, l): return [xorxor(ia, ja, la) for ia, ja, la, in zip(i, j, l)]

def maj(i,j,k): return max([i,j,], key=[i,j,k].count)

def rotr(x, n): return x[-n:] + x[:-n]

def shr(x, n): return n * [0] + x[:-n]

def add(i, j):
    length = len(i)
    sums = list(range(length))
    c = 0
    for x in range(length-1,-1,-1):
        sums[x] = xorxor(i[x], j[x], c)
        c = maj(i[x], j[x], c)
    return sums