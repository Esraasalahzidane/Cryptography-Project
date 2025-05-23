import hmac
import hashlib

def generate_hmac(key, message):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def brute_force_hmac(message, target_hmac):
    for guess in range(10000):  # بنجرب المفاتيح من 0000 إلى 9999
        key_guess = str(guess).zfill(4)
        h = generate_hmac(key_guess, message)
        if h == target_hmac:
            print(f"Found key: {key_guess}")
            return key_guess
    print(" Key not found.")
    return None

#  التجربه ي دكتور الى عملنا عليها الbrute force
true_key = "0420"
message = "This is a secret message"
target_hmac = generate_hmac(true_key, message)

print(f"HMAC to break: {target_hmac}\n")

brute_force_hmac(message, target_hmac)
