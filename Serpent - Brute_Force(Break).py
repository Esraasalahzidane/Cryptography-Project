from numba import njit
import time

@njit
def simple_sbox(block):
    return block ^ 0xFFFFFFFFFFFFFFFF

@njit
def add_round_key(block, round_key):
    return block ^ round_key

@njit
def linear_transform(block):
    return ((block << 3) & 0xFFFFFFFFFFFFFFFF) | (block >> (64 - 3))

@njit
def serpent_encrypt(plain_text, key, rounds=4):
    block = plain_text
    round_keys = [key ^ (i * 0x1111111111111111) for i in range(rounds + 1)]
    for i in range(rounds):
        block = add_round_key(block, round_keys[i])
        block = simple_sbox(block)
        if i < rounds - 1:
            block = linear_transform(block)
    block = add_round_key(block, round_keys[-1])
    return block

@njit
def serpent_decrypt(cipher_text, key, rounds=4):
    block = cipher_text
    round_keys = [key ^ (i * 0x1111111111111111) for i in range(rounds + 1)]
    block = add_round_key(block, round_keys[-1])
    for i in range(rounds - 1, -1, -1):
        if i < rounds - 1:
            block = linear_transform(block)
        block = simple_sbox(block)
        block = add_round_key(block, round_keys[i])
    return block

def brute_force_attack(encrypted_text, known_plain_text, rounds=4, max_key=2**24):
   
    for key in range(max_key):
        decrypted = serpent_decrypt(encrypted_text, key, rounds)
        if decrypted == known_plain_text:
            return key
    return None


plain_text_bytes = b"Serpent8"  
plain_text = int.from_bytes(plain_text_bytes, "big")

key = 0x123456  
encrypted = serpent_encrypt(plain_text, key)

print(f"Encrypted: {hex(encrypted)}")

start = time.time()
found_key = brute_force_attack(encrypted, plain_text, max_key=2**24)
end = time.time()

if found_key is not None:
    print(f"Key found: {hex(found_key)}")
else:
    print("Key not found")

print(f"Time taken: {end - start:.2f} seconds")
