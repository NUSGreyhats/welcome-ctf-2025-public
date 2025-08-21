import base64
import re

def solve():
    with open('../distrib/shy_zipper.zip', 'rb') as f:
        data = f.read()
        
    eocd_sign = b'PK\x05\x06'
    eocd_offset = data.find(eocd_sign)
    
    comment_len = int.from_bytes(data[eocd_offset + 20 : eocd_offset + 22], 'little')
    eocd_end = eocd_offset + 22 + comment_len
    
    # extra data after EOCD
    if len(data) > eocd_end:
        extra_data = data[eocd_end:]
        base64_pattern = rb'[A-Za-z0-9+/]+={0,2}'
        matches = re.findall(base64_pattern, extra_data)
        
        for match in matches:
            try:
                decoded = base64.b64decode(match)
                if b'grey' in decoded:
                    print(f"Found flag: {decoded.decode()}")
                    return
            except:
                pass

if __name__ == '__main__':
    solve()