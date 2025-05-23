import hmac
import hashlib


def generate_hmac(key, message):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


def verify_hmac(key, message, expected_hmac):
    generated_hmac = generate_hmac(key, message)
    return hmac.compare_digest(generated_hmac, expected_hmac)


if __name__ == "__main__":
    key = "mysecretkey" 
    message = "This is a secret message" 
    
    
    hmac_signature = generate_hmac(key, message)
    print(f"HMAC Signature: {hmac_signature}")
    
    
    if verify_hmac(key, message, hmac_signature):
        print("HMAC is valid! Message is authentic.\n")
    else:
        print("HMAC is invalid! Message may have been tampered with.")
