import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


def generate_hmac(key, message):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


def verify_hmac(key, message, expected_hmac):
    generated_hmac = generate_hmac(key, message)
    return hmac.compare_digest(generated_hmac, expected_hmac)


def encrypt_aes(key, plaintext):
    key = key.ljust(16, '0') 
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.b64encode(cipher.iv + ciphertext).decode('utf-8')


def decrypt_aes(key, encrypted):
    key = key.ljust(16, '0')  
    encrypted_bytes = base64.b64decode(encrypted)
    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    return decrypted


if __name__ == "__main__":
    secret_key = "mysecretkey" 
    message = "This is a secret message"  
    
   
    hmac_signature = generate_hmac(secret_key, message)
    print(f"HMAC Signature: {hmac_signature}")
    
 
    if verify_hmac(secret_key, message, hmac_signature):
        print("HMAC is valid! Message is authentic.")
    else:
        print("HMAC is invalid! Message may have been tampered with.")
    
    
    encrypted_message = encrypt_aes(secret_key, message)
    print(f"Encrypted Message: {encrypted_message}")
    
 
    decrypted_message = decrypt_aes(secret_key, encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")
