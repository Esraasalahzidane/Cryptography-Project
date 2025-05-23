def encrypt(plain_text, key): 
   
    v0, v1 = plain_text[0], plain_text[1]
    key0, key1, key2, key3 = key
    delta = 0x9e3779b9
    sum = 0

    for _ in range(32):  
        sum = (sum + delta) & 0xffffffff
        v0 += (((v1 << 4) + key0) ^ (v1 + sum) ^ ((v1 >> 5) + key1)) & 0xffffffff
        v0 = v0 & 0xffffffff
        v1 += (((v0 << 4) + key2) ^ (v0 + sum) ^ ((v0 >> 5) + key3)) & 0xffffffff
        v1 = v1 & 0xffffffff

    return [v0, v1]


def decrypt(cipher_text, key):
    
    v0, v1 = cipher_text[0], cipher_text[1]
    key0, key1, key2, key3 = key
    delta = 0x9e3779b9
    sum = delta * 32 

    for _ in range(32):  
        v1 -= (((v0 << 4) + key2) ^ (v0 + sum) ^ ((v0 >> 5) + key3)) & 0xffffffff
        v1 = v1 & 0xffffffff
        v0 -= (((v1 << 4) + key0) ^ (v1 + sum) ^ ((v1 >> 5) + key1)) & 0xffffffff
        v0 = v0 & 0xffffffff
        sum -= delta
        sum = sum & 0xffffffff

    return [v0, v1]


def string_to_int_list(input_string):

    input_bytes = input_string.encode('utf-8')
    return [int.from_bytes(input_bytes[:4], 'big'), int.from_bytes(input_bytes[4:8], 'big')]


def int_list_to_string(int_list):
   
    return (int_list[0].to_bytes(4, 'big') + int_list[1].to_bytes(4, 'big')).decode('utf-8')


def main():
  
    plain_text = "abcdefgh" 
    key = [1234, 5678, 9101, 1121] 

 
    plain_text_int_list = string_to_int_list(plain_text)


    encrypted = encrypt(plain_text_int_list, key)
    print(f"Encrypted text: {encrypted}")

   
    decrypted = decrypt(encrypted, key)
    decrypted_text = int_list_to_string(decrypted)
    print(f"Decrypted text: {decrypted_text}")


if __name__ == "__main__":
    main()
