from itertools import cycle

with open("../secret.txt", "r") as f:
    FLAG = f.read().strip().encode()

class CAK256:
    def __init__(self, seed: int = 1):
        if seed == 0:
            raise ValueError("Seed cannot be zero for xorshift")
        
        self.state = [0] * 4
        temp_seed = seed
        
        for i in range(4):
            temp_seed = temp_seed ^ (temp_seed >> 12)
            temp_seed = temp_seed ^ (temp_seed << 25) 
            temp_seed = temp_seed ^ (temp_seed >> 27)
            temp_seed = (temp_seed * 0x2545F4914F6CDD1D) & ((1 << 128) - 1)
            self.state[i] = temp_seed if temp_seed != 0 else 0x123456789ABCDEF0 + i
        
        self.original_state = self.state.copy()
        
        self.shift_a = 23
        self.shift_b = 17
        self.shift_c = 26
    
    def _state_to_int(self) -> int:
        result = 0
        for i in range(4):
            result |= self.state[i] << (64 * i)
        return result
    
    def _int_to_state(self, value: int):
        for i in range(4):
            self.state[i] = (value >> (64 * i)) & ((1 << 128) - 1)
    
    def next(self) -> int:
        state_int = self._state_to_int()
        
        # I'm swapping them so fast you can't see the bits at all! >:D
        state_int ^= state_int << self.shift_a
        state_int ^= state_int >> self.shift_b
        state_int ^= state_int << self.shift_c
        
        state_int &= ((1 << 256) - 1)
        
        self._int_to_state(state_int)
        
        return self.state[0]
    
    def reset(self):
        self.state = self.original_state.copy()
    
    def get_state_hex(self) -> str:
        return "".join(f"{word:016x}" for word in self.state)
    
    def get_state_bytes(self) -> bytes:
        return b"".join(word.to_bytes(8, 'big') for word in self.state)
    
if __name__ == "__main__":
    rng = CAK256(12345)

    # Good luck computing this state! ~N00bcak
    large_skip = (1 << 63) - 1
    for _ in range(large_skip):
        rng.next()
    xor_key = rng.get_state_bytes()

    assert len(xor_key) >= len(FLAG), f"XOR key length is too short! {len(xor_key)} < {len(FLAG)}"
    enc = bytes([a ^ b for a, b in zip(cycle(xor_key), FLAG)])
    with open("../distrib/flag.enc", "w") as f:
        f.write(enc.hex())