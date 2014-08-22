#
# Copyright (c) 2014 iAchieved.it LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#

from binascii import hexlify
from hashlib import sha1
from bitstring import BitStream

def uhexlify(h):
    s = hexlify(h).upper()
    return " ".join(s[i:i+8] for i in range(0, len(s), 8))

def bytes_to_long(s):
    n = ord(s[0])
    for b in ( ord(x) for x in s[1:] ):
        n = (n << 8) | b
    return n
  
def long_to_bytes(n):
    l = list()
    x = 0
    off = 0
    while x != n:
        b = (n >> off) & 0xFF
        l.append( chr(b) )
        x = x | (b << off)
        off += 8
    l.reverse()
    return ''.join(l)

##
#
#    Function:  calc_k
# Description:  Performs calculation of k
#      Inputs:  N : long
#               g : long
#     Returns:  H(N | g) : long
#
def calc_k(N, g):
    nhex = hexlify(long_to_bytes(N))

    nlen = len(nhex)
    if len(nhex) % 2 != 0:
        nlen += 1 # Extra pad if odd
    ghex = hexlify(long_to_bytes(g))

    hashin = '0' * (nlen - len(nhex)) + nhex \
           + '0' * (nlen - len(ghex)) + ghex

    k = int(sha1(BitStream(hex=hashin).bytes).hexdigest(), 16) % N
    return k

##
#
# username:  UTF-8 string
# password:  UTF-8 string
# salt:      long
#
def calc_x(username, password, salt):
    shex = hexlify(long_to_bytes(salt))
    if len(shex) % 2 != 0:
        spad = '0'
    else:
        spad = ''

    hashin = spad + shex + sha1(username + ":" + password).hexdigest()
    x = int(sha1(BitStream(hex=hashin).bytes).hexdigest(), 16)
    return x

#
#  calc_u
#  A : long
#  B : long
#  N : long
#
# Returns:  long
def calc_u(A, B, N):
    nhex = hexlify(long_to_bytes(N))
    nlen = 2 * ((len(nhex) * 4 + 7) >> 3)
    Ahex = hexlify(long_to_bytes(A))
    Bhex = hexlify(long_to_bytes(B))
    hashin = '0' * (nlen - len(Ahex)) + Ahex \
           + '0' * (nlen - len(Bhex)) + Bhex

    return int(sha1(BitStream(hex=hashin).bytes).hexdigest(), 16)

#
# calc_M
#
def calc_M(N, g, username, salt, A, B, K):
    M = sha1()
    M.update(calc_HNxorHg())
    M.update(sha1(username).digest())
    M.update(long_to_bytes(salt))
    M.update(long_to_bytes(A))
    M.update(long_to_bytes(B))
    M.update(K)
    return M.digest()

def calc_HNxorHg(N, g):
    nhex = hexlify(long_to_bytes(N))
    print nhex
    ghex = hexlify(long_to_bytes(g))
    print ghex
    hn = sha1(BitStream(hex=nhex).bytes).hexdigest()
    hg = sha1(BitStream(hex=ghex).bytes).hexdigest()
    print hn
    print hg
    hnXORhg = BitStream(hex=hn) ^ BitStream(hex=hg)
    return hnXORhg.bytes
    


N = 167609434410335061345139523764350090260135525329813904557420930309800865859473551531551523800013916573891864789934747039010546328480848979516637673776605610374669426214776197828492691384519453218253702788022233205683635831626913357154941914129985489522629902540768368409482248290641036967659389658897350067939L

g = 2



k = calc_k(N, g)

print "M2 = %s " % calc_M2(N,g)

print "k = %s" % uhexlify(long_to_bytes(k))

# Test vector salt
salt = int("BEB25379D1A8581EB5A727673A2441EE", 16)
    
x = calc_x("alice", "password123", salt)

print "x = %s" % uhexlify(long_to_bytes(x))

v = pow(g, x, N)

print "v = %s" % uhexlify(long_to_bytes(v))

a = int("60975527035CF2AD1989806F0407210BC81EDC04E2762A56AFD529DDDA2D4393", 16)
b = int("E487CB59D31AC550471E81F00F6928E01DDA08E974A004F49E61F5D105284D20", 16)

B = (pow(g, b, N) + k * v) % N # B = (g^b + kv) mod N

print "B = %s" % uhexlify(long_to_bytes(B))

A = pow(g, a, N)

print "A = %s" % uhexlify(long_to_bytes(A))


username = 'alice'
password = 'password123'

u = calc_u(A, B, N)

print "u = %s" % uhexlify(long_to_bytes(u))

Sc = pow((B + N*k - pow(g, x, N)*k) % N, x * u + a, N)

print "Sc = %s" % uhexlify(long_to_bytes(Sc))

Ss = pow((pow(v, u, N) * A % N), b, N) # S = ((v^u * A)^b) % N

print "Ss = %s" % uhexlify(long_to_bytes(Ss))

K = sha1(long_to_bytes(Ss)).digest()

print BitStream(bytes=calc_M(N,g,"alice",salt,A, B, K))
