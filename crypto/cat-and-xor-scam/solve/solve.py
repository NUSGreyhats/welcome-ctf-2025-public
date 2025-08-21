# Yes. This is vibecoded.
# Pretty impressive considering this was cooked in the span of 20 minutes.
# I suspect there will be unexpected vulns, so this challenge will 
# hopefully be fodder for the noob teams.

from typing import List, Tuple, Set, Dict
from tqdm import tqdm
from itertools import cycle

class CAK256:
    def __init__(self, seed: int = 1):
        """Initialize with a seed. Creates a 512-bit state from the seed."""
        if seed == 0:
            raise ValueError("Seed cannot be zero for xorshift")
        
        # Initialize 512-bit state (8 × 64-bit words)
        # Use a better seed expansion algorithm
        self.state = [0] * 4
        temp_seed = seed
        
        # Use a more sophisticated seed expansion to ensure good initial entropy
        for i in range(4):
            # Multiple rounds of mixing to ensure each 64-bit word is well-initialized
            temp_seed = temp_seed ^ (temp_seed >> 12)
            temp_seed = temp_seed ^ (temp_seed << 25) 
            temp_seed = temp_seed ^ (temp_seed >> 27)
            temp_seed = (temp_seed * 0x2545F4914F6CDD1D) & ((1 << 128) - 1)
            self.state[i] = temp_seed if temp_seed != 0 else 0x123456789ABCDEF0 + i
        
        self.original_state = self.state.copy()
        
        # Better parameters for 512-bit xorshift - these are chosen for maximal period
        # and good statistical properties in higher dimensions
        self.shift_a = 23  # First left shift
        self.shift_b = 17  # Right shift  
        self.shift_c = 26  # Second left shift
    
    def _state_to_int(self) -> int:
        """Convert 8-word state to single 512-bit integer."""
        result = 0
        for i in range(4):
            result |= self.state[i] << (64 * i)
        return result
    
    def _int_to_state(self, value: int):
        """Convert 512-bit integer back to 8-word state."""
        for i in range(4):
            self.state[i] = (value >> (64 * i)) & ((1 << 128) - 1)
    
    def next(self) -> int:
        """
        Generate next random number using xorshift512 with strong parameters.
        
        The algorithm applies three XOR-shift operations in sequence:
        1. Left shift by 23, then XOR
        2. Right shift by 17, then XOR  
        3. Left shift by 26, then XOR
        
        These parameters are specifically chosen for 512-bit state to ensure
        maximal period and excellent statistical properties.
        """
        # Work with full 512-bit state as single integer for bit operations
        state_int = self._state_to_int()
        
        # Apply the three xorshift transformations with strong parameters
        state_int ^= state_int << self.shift_a  # Left shift by 23
        state_int ^= state_int >> self.shift_b  # Right shift by 17
        state_int ^= state_int << self.shift_c  # Left shift by 26
        
        # Mask to keep within 512 bits
        state_int &= ((1 << 256) - 1)
        
        # Convert back to state array
        self._int_to_state(state_int)
        
        # Return the first 64 bits as the random output
        return self.state[0]
    
    def reset(self):
        """Reset to original state."""
        self.state = self.original_state.copy()
    
    def get_state_hex(self) -> str:
        """Get current state as hex string for comparison."""
        return "".join(f"{word:016x}" for word in self.state)
    
    def get_state_bytes(self) -> bytes:
        """Get current state as bytes for XOR operations."""
        return b"".join(word.to_bytes(8, 'big') for word in self.state)
    
    def _build_transformation_matrix_correct(self) -> List[Tuple[int, int]]:
        """
        Build the correct 256x256 transformation matrix for our xorshift algorithm.
        
        This is the crucial fix! Each transformation step must be applied in sequence,
        not as independent operations. The matrix represents the composition of
        all three transformations: T3(T2(T1(x))) where:
        - T1: x ^= x << shift_a
        - T2: x ^= x >> shift_b  
        - T3: x ^= x << shift_c
        """
        # We'll build this by tracing how each input bit affects each output bit
        # through the complete sequence of transformations
        
        matrix_ones = set()  # Use set to avoid duplicates
        
        print("Building transformation matrix...")
        for input_bit in tqdm(range(256), desc="Processing input bits"):
            # Create a basis vector with only this input bit set
            test_vector = [0] * 256
            test_vector[input_bit] = 1
            
            # Apply the complete xorshift transformation sequence
            transformed = self._apply_single_xorshift_to_bitvector(test_vector)
            
            # Record which output bits were affected by this input bit
            for output_bit in range(256):
                if transformed[output_bit] == 1:
                    matrix_ones.add((output_bit, input_bit))
        
        return list(matrix_ones)
    
    def _apply_single_xorshift_to_bitvector(self, bitvector: List[int]) -> List[int]:
        """
        Apply one complete xorshift transformation to a bit vector.
        
        This implements the exact same sequence as our next() method,
        but works on individual bit vectors for matrix construction.
        """
        # Convert bit vector to integer
        value = 0
        for i, bit in enumerate(bitvector):
            if bit:
                value |= 1 << i
        
        # Apply the exact same transformations as in next()
        value ^= value << self.shift_a  # T1
        value ^= value >> self.shift_b  # T2  
        value ^= value << self.shift_c  # T3
        value &= ((1 << 256) - 1)  # Mask to 256 bits
        
        # Convert back to bit vector
        result = [0] * 256
        for i in range(256):
            if value & (1 << i):
                result[i] = 1
        
        return result
    
    def _sparse_matrix_multiply_gf2(self, vector: List[int], matrix_ones: List[Tuple[int, int]]) -> List[int]:
        """
        Multiply vector by sparse matrix in GF(2) arithmetic.
        
        In GF(2), addition is XOR operation, so we XOR contributions
        from each non-zero matrix entry.
        """
        result = [0] * 256
        
        # For each non-zero entry in the matrix, add its contribution
        for row, col in matrix_ones:
            # In GF(2): result[row] += matrix[row][col] * vector[col]
            # Since matrix[row][col] = 1, this becomes: result[row] ^= vector[col]
            result[row] ^= vector[col]
        
        return result
    
    def _sparse_matrix_multiply_matrices(self, A_ones: List[Tuple[int, int]], 
                                       B_ones: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Multiply two sparse matrices A and B, returning C = A × B in GF(2).
        
        This is the heart of fast matrix exponentiation. We convert to
        dictionary representation for efficient computation, then convert back.
        """
        # Convert to dictionary format for efficient access
        A_dict = {}
        for row, col in A_ones:
            if row not in A_dict:
                A_dict[row] = set()
            A_dict[row].add(col)
        
        B_dict = {}
        for row, col in B_ones:
            if row not in B_dict:
                B_dict[row] = set()
            B_dict[row].add(col)
        
        # Compute C = A × B
        C_dict = {}
        
        # For each row i in A
        for i in A_dict:
            # For each column k where A[i][k] = 1
            for k in A_dict[i]:
                # For each column j where B[k][j] = 1
                if k in B_dict:
                    for j in B_dict[k]:
                        # C[i][j] ^= A[i][k] * B[k][j] = 1 * 1 = 1
                        if i not in C_dict:
                            C_dict[i] = set()
                        
                        # XOR operation in GF(2) - toggle the bit
                        if j in C_dict[i]:
                            C_dict[i].remove(j)  # 1 ⊕ 1 = 0
                        else:
                            C_dict[i].add(j)     # 0 ⊕ 1 = 1
        
        # Convert back to list of tuples, removing empty sets
        result = []
        for row in C_dict:
            for col in C_dict[row]:
                result.append((row, col))
        
        return result
    
    def _matrix_power_sparse(self, matrix_ones: List[Tuple[int, int]], n: int) -> List[Tuple[int, int]]:
        """
        Compute A^n using binary exponentiation with sparse matrices.
        
        This implements the standard "exponentiation by squaring" algorithm
        but adapted for sparse matrices in GF(2) arithmetic.
        """
        if n == 0:
            # Return identity matrix
            return [(i, i) for i in range(256)]
        
        if n == 1:
            return matrix_ones.copy()
        
        # Binary exponentiation: A^n = A^(binary representation of n)
        result = [(i, i) for i in range(256)]  # Identity matrix
        base = matrix_ones.copy()
        
        print(f"Computing matrix power {n} using binary exponentiation...")
        with tqdm(total=n.bit_length(), desc="Matrix exponentiation") as pbar:
            while n > 0:
                if n & 1:  # If current bit of n is 1
                    result = self._sparse_matrix_multiply_matrices(result, base)
                    pbar.set_postfix({"result_entries": len(result)})
                
                base = self._sparse_matrix_multiply_matrices(base, base)
                n >>= 1
                pbar.update(1)
        
        return result
    
    def _matrix_power_multiply(self, vector: List[int], n: int) -> List[int]:
        """
        The corrected implementation: multiply vector by A^n using sparse methods.
        
        This is now mathematically correct because we build the transformation
        matrix by actually tracing the effect of each input bit through the
        complete xorshift sequence.
        """
        if n == 0:
            return vector.copy()
        
        # Build the correct transformation matrix
        print("Building transformation matrix for skip-ahead...")
        matrix_ones = self._build_transformation_matrix_correct()
        
        print(f"Matrix has {len(matrix_ones)} non-zero entries out of {256*256} total")
        print(f"Sparsity: {100 * (1 - len(matrix_ones)/(256*256)):.2f}%")
        
        # Compute A^n
        matrix_power = self._matrix_power_sparse(matrix_ones, n)
        
        print(f"A^{n} has {len(matrix_power)} non-zero entries")
        
        # Multiply vector by A^n
        return self._sparse_matrix_multiply_gf2(vector, matrix_power)
    
    def skip_ahead(self, n: int):
        """
        Skip ahead n steps using the corrected sparse matrix implementation.
        
        Now this should produce exactly the same result as calling next() n times!
        """
        if n == 0:
            return
        
        print(f"Skipping ahead {n} steps...")
        
        # Convert current state to bit vector
        current_int = self._state_to_int()
        state_vector = [(current_int >> i) & 1 for i in range(256)]
        
        # Apply A^n to the state vector
        result_vector = self._matrix_power_multiply(state_vector, n)
        
        # Convert back to integer and then to state
        result_int = sum(bit << i for i, bit in enumerate(result_vector))
        self._int_to_state(result_int)

def test_correctness_with_progress():
    """
    Comprehensive test to verify skip-ahead produces identical results to sequential generation.
    """
    print("=== Correctness Verification Test ===\n")
    
    # Test with different skip distances
    test_cases = [1, 3, 7, 31, 127, 1023, 65537]
    
    for skip_n in test_cases:
        print(f"\nTesting skip distance: {skip_n}")
        
        # Create two identical generators
        rng_sequential = CAK256(12345)
        rng_skip = CAK256(12345)
        
        # Generate numbers sequentially
        print("Generating sequentially...")
        sequential_results = []
        for i in tqdm(range(skip_n), desc="Sequential generation"):
            sequential_results.append(rng_sequential.next())
        
        # Get the state after sequential generation
        sequential_final_state = rng_sequential.get_state_hex()
        
        # Skip ahead directly
        print("Skipping ahead...")
        rng_skip.skip_ahead(skip_n)
        skip_final_state = rng_skip.get_state_hex()
        
        # Compare final states
        states_match = sequential_final_state == skip_final_state
        print(f"Final states match: {states_match}")
        
        if states_match:
            print("✓ Test PASSED")
        else:
            print("✗ Test FAILED")
            print(f"Sequential final state: {sequential_final_state[:50]}...")
            print(f"Skip-ahead final state: {skip_final_state[:50]}...")
            return False
        
        # Test that next values are also identical
        next_sequential = rng_sequential.next()
        next_skip = rng_skip.next()
        
        print(f"Next values match: {next_sequential == next_skip}")
        if next_sequential != next_skip:
            print(f"Sequential next: {next_sequential:016x}")
            print(f"Skip next: {next_skip:016x}")
            return False
    
    print("\n All tests PASSED! Skip-ahead implementation is correct.")
    return True

if __name__ == "__main__":
    # Run correctness tests
    assert test_correctness_with_progress(), "Correctness tests failed - please check implementation!"
    print("\n=== Performance Demo ===")
    
    rng = CAK256(12345)
    print(f"Initial state: {rng.get_state_hex()}")
    
    large_skip = (1 << 63) - 1
    print(f"\nSkipping ahead {large_skip} steps...")
    rng.skip_ahead(large_skip)
    xor_key = rng.get_state_bytes()
    print(f"Final state: {xor_key}")

    with open("../distrib/flag.enc", "r") as f:
        ENC_FLAG = bytes.fromhex(f.read().strip())

    assert len(xor_key) >= len(ENC_FLAG), f"XOR key length is too short! {len(xor_key)} < {len(ENC_FLAG)}"
    dec = bytes([a ^ b for a, b in zip(cycle(xor_key), ENC_FLAG)])
    with open("../secret.txt", "r") as f:
        FLAG = f.read().strip().encode()
    assert dec == FLAG, "Decrypted flag does not match the original!"
    print("Decryption successful! Flag:", dec.decode())