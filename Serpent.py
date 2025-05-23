def simple_sbox(block):
    
    return block ^ 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  

def add_round_key(block, round_key):
    return block ^ round_key

def linear_transform(block):
  
    return ((block << 3) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) | (block >> (128 - 3))

def serpent_encrypt(plain_text, key, rounds=4):
    block = plain_text
    round_keys = [key ^ (i * 0x11111111111111111111111111111111) for i in range(rounds + 1)]

    for i in range(rounds):
        block = add_round_key(block, round_keys[i])
        block = simple_sbox(block)
        if i < rounds - 1:
            block = linear_transform(block)

    block = add_round_key(block, round_keys[-1])
    return block

def serpent_decrypt(cipher_text, key, rounds=4):
    block = cipher_text
    round_keys = [key ^ (i * 0x11111111111111111111111111111111) for i in range(rounds + 1)]

    block = add_round_key(block, round_keys[-1])

    for i in reversed(range(rounds)):
        if i < rounds - 1:
            block = linear_transform(block)  
        block = simple_sbox(block)
        block = add_round_key(block, round_keys[i])

    return block


plain_text = int.from_bytes(b"SerpentTest1234", "big")
key = int.from_bytes(b"KeyForSerpent16", "big")

encrypted = serpent_encrypt(plain_text, key)
decrypted = serpent_decrypt(encrypted, key)

print(f"Encrypted: {hex(encrypted)}")
print(f"Decrypted: {decrypted.to_bytes(16, 'big')}")
