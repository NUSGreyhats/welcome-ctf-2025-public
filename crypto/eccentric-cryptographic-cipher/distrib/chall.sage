from Crypto.Util.number import bytes_to_long, getStrongPrime
from Crypto.Random.random import getrandbits
from random import shuffle

import json 

load('messages.sage')

NBITS = 1024
p = getStrongPrime(NBITS)
q = getStrongPrime(NBITS)
n = p * q

phi = (p - 1) * (q - 1)
for _ in range(100_000):
    e = getrandbits(n.bit_length() // 2)
    if gcd(e, phi) != 1:
        continue
    d = pow(e, -1, phi)
    if d ** (1 / 0.292) > n:
        break

messages = get_messages(p, q, e)

shuffle(messages)
encs = []
for msg in messages:
    pt = bytes_to_long(msg)
    ct = pow(pt, e, n)
    encs.append({
        'ct': ct,
    })
    if b'grey{' not in msg:
        encs[-1]['pt'] = int(pt)


with open('chall.json', 'w') as f:
    f.write(json.dumps({
        'n': n,
        'e': e,
        'encs': encs,
    }, indent=4).replace(' ', ''))