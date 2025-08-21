#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long

flag = b"grey{REDACTED}" 

e = 65537
p = 0 # REDACTED
q = 0 # REDACTED
n = p * q

m = bytes_to_long(flag)
c = pow(m, e, n)

# Print safe public info
print("n =", n)
print("e =", e)
print("c =", c) # ciphertext