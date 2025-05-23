def encrypt(plain_text, key): 
    v0, v1 = plain_text[0], plain_text[1]
    key0, key1, key2, key3 = key
    delta = 0x9e3779b9
    sum = 0

    for _ in range(32):  
        sum = (sum + delta) & 0xffffffff
        v0 = (v0 + (((v1 << 4) + key0) ^ (v1 + sum) ^ ((v1 >> 5) + key1))) & 0xffffffff
        v1 = (v1 + (((v0 << 4) + key2) ^ (v0 + sum) ^ ((v0 >> 5) + key3))) & 0xffffffff

    return [v0, v1]

def decrypt(cipher_text, key):
    v0, v1 = cipher_text[0], cipher_text[1]
    key0, key1, key2, key3 = key
    delta = 0x9e3779b9
    sum = (delta * 32) & 0xffffffff

    for _ in range(32):  
        v1 = (v1 - (((v0 << 4) + key2) ^ (v0 + sum) ^ ((v0 >> 5) + key3))) & 0xffffffff
        v0 = (v0 - (((v1 << 4) + key0) ^ (v1 + sum) ^ ((v1 >> 5) + key1))) & 0xffffffff
        sum = (sum - delta) & 0xffffffff

    return [v0, v1]

def string_to_int_list(input_string):
    input_bytes = input_string.encode('utf-8')
    return [int.from_bytes(input_bytes[:4], 'big'), int.from_bytes(input_bytes[4:8], 'big')]

def int_list_to_string(int_list):
    return (int_list[0].to_bytes(4, 'big') + int_list[1].to_bytes(4, 'big')).decode('utf-8')

def brute_force(encrypted, known_plaintext):
    known_int = string_to_int_list(known_plaintext)
    count = 0
    for k0 in range(1000):
        for k1 in range(1000):
            for k2 in range(1000):
                for k3 in range(1000):
                    key = [k0, k1, k2, k3]
                    decrypted = decrypt(encrypted, key)
                    count += 1
                    if count % 100000 == 0:
                        print(f"Trying keys... Tried {count} keys so far")
                    if decrypted == known_int:
                        print(f"Key found: {key} after trying {count} keys")
                        return key
    print("Key not found in range 0-999 for each key part")
    return None

def main():
    plain_text = "abcdefgh"
    key = [123, 456, 789, 101]

    plain_text_int_list = string_to_int_list(plain_text)
    encrypted = encrypt(plain_text_int_list, key)
    print(f"Encrypted text: {encrypted}")

    found_key = brute_force(encrypted, plain_text)
    if found_key:
        decrypted = decrypt(encrypted, found_key)
        decrypted_text = int_list_to_string(decrypted)
        print(f"Decrypted text with found key: {decrypted_text}")
    else:
        print("Failed to find the key.")

if __name__ == "__main__":
    main()
