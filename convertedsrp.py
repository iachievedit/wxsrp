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

def calc_x(username, password, salt):
    shex = hexlify(long_to_bytes(salt))
    if len(shex) % 2 != 0:
        spad = '0'
    else:
        spad = ''

    hashin = spad + shex + sha1(username + ":" + password).hexdigest()
    x = int(sha1(BitStream(hex=hashin).bytes).hexdigest(), 16)
    return x

N = 167609434410335061345139523764350090260135525329813904557420930309800865859473551531551523800013916573891864789934747039010546328480848979516637673776605610374669426214776197828492691384519453218253702788022233205683635831626913357154941914129985489522629902540768368409482248290641036967659389658897350067939L

g = 2

k = calc_k(N, g)

print hexlify(long_to_bytes(k))
    
x = calc_x("alice", "password123", bytes_to_long(BitStream(hex="BEB25379 D1A8581E B5A72767 3A2441EE").bytes))

print hexlify(long_to_bytes(x))
