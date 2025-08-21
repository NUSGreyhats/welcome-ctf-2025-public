import json
from math import gcd
from Crypto.Util.number import long_to_bytes, bytes_to_long

with open('distrib/chall.json', 'r') as f:
    data = json.load(f)
    n = data['n']
    e = data['e']
    encs = data['encs']
    factors = None
    for enc in encs:
        ct = enc['ct']
        # Attempt to find fixed point with gcd
        if gcd(ct + 1, n) != 1:
            print("Found fixed point:", ct + 1)
            factors = (gcd(ct + 1, n), n // gcd(ct + 1, n))
            break
        elif gcd(ct - 1, n) != 1:
            print("Found fixed point:", ct - 1)
            factors = (gcd(ct - 1, n), n // gcd(ct - 1, n))
            break
    if factors:
        p, q = factors
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        print("Decrypted messages:")
        for enc in encs:
            pt = pow(enc['ct'], d, n)
            print(long_to_bytes(pt))
        print("p:", p)
        print("q:", q)
        print("d:", d)
        print("n:", n)
        print("e:", e)