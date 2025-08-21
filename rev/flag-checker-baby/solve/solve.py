enc = [68, 47, 70, 42, 40, 48, 58, 62, 49, 61, 70, 12, 62, 70, 59, 54, 12, 47, 70, 51, 46]

result = []
for c in enc:
    result.append((c - 7) & 0xFF ^ 0x5a)
   
print("".join([chr(i) for i in result]))
