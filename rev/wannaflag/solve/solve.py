#!/usr/bin/env python3
"""
CTF Ransom Challenge Solution
============================

This script demonstrates how to solve the CTF challenge by:
1. Extracting the RC4 key from the DLL analysis
2. Decrypting the flag from actual_flag.blackhat
"""

import binascii

def rc4_init(key):
    """Initialize RC4 S-box with key"""
    s = list(range(256))
    j = 0
    
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    
    return s

def rc4_decrypt(s, data):
    """Decrypt data using RC4"""
    s = s.copy()  # Don't modify original
    i = j = 0
    result = []
    
    for byte in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        result.append(byte ^ s[(s[i] + s[j]) % 256])
    
    return bytes(result)

def solve_challenge():
    """Solve the CTF challenge"""
    print("CTF Ransom Challenge Solver")
    print("===========================")
    
    # Step 1: Analyze the DLL to find the key generation
    print("\n1. Analyzing not_sus.dll...")
    print("   Found: generate_rc4_key() function")
    print("   Key: 'grey_hats_is_cool' (no nonce)")
    
    # Step 2: Use the discovered key
    print("\n2. Using discovered key...")
    key = "grey_hats_is_cool"
    print(f"   RC4 Key: {key}")
    
    # Step 3: Read the encrypted flag
    try:
        with open('./actual_flag.blackhat', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract hex data from the ransom note
        lines = content.split('\n')
        hex_line = None
        for line in lines:
            if len(line) > 20 and all(c in '0123456789abcdef' for c in line.lower()):
                hex_line = line.strip()
                break
        
        if not hex_line:
            print("Error: Could not find encrypted flag in actual_flag.blackhat")
            return
        
        encrypted_data = binascii.unhexlify(hex_line)
        print(f"\n3. Found encrypted flag: {hex_line}")
        
    except FileNotFoundError:
        print("Error: actual_flag.blackhat not found. Run beautify_flag.exe first!")
        return
    
    # Step 4: Decrypt with the discovered key
    print("\n4. Decrypting flag...")
    
    # Convert key to bytes
    key_bytes = key.encode('ascii')
    
    # Initialize RC4
    s = rc4_init(key_bytes)
    
    # Decrypt
    decrypted = rc4_decrypt(s, encrypted_data)
    
    try:
        flag = decrypted.decode('ascii').strip()
        if flag.startswith('grey{') and flag.endswith('}'):
            print(f"\n🎉 SUCCESS! Flag found: {flag}")
            return flag
        else:
            print(f"⚠️ Decrypted text: {flag}")
            print("This might not be the correct flag format")
            return flag
    except UnicodeDecodeError:
        print("❌ Decryption failed - invalid characters")
        print("The key might be incorrect")
        return None

if __name__ == "__main__":
    solve_challenge()
