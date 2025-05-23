import struct

# نسخ مبسطة من جداول P و S (اختصرتهم للتجربة فقط)
P = [
    0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344,
    0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89,
    0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C,
    0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917,
    0x9216D5D9, 0x8979FB1B
]

S = [[0xD1310BA6] * 256] * 4  # جداول S وهمية (بس علشان الكود يشتغل)

def F(x):
    # دالة F مبسطة (في الحقيقة بتستخدم الـ S-boxes الأربعة)
    return ((x << 1) ^ (x >> 1)) & 0xFFFFFFFF

def encrypt_block(left, right):
    for i in range(16):
        left = left ^ P[i]
        right = right ^ F(left)
        left, right = right, left
    left, right = right, left
    right = right ^ P[16]
    left = left ^ P[17]
    return left, right

def decrypt_block(left, right):
    for i in reversed(range(2, 18)):
        left = left ^ P[i]
        right = right ^ F(left)
        left, right = right, left
    left, right = right, left
    right = right ^ P[1]
    left = left ^ P[0]
    return left, right

def brute_force_p0(ciphertext, known_plaintext):
    right = struct.unpack(">I", known_plaintext[4:])[0]
    target_right = struct.unpack(">I", ciphertext[4:])[0]

    for guess in range(0x00000000, 0x0000FFFF):  # نضيق المدى دا للتجربة
        trial_right = right ^ F(right ^ guess)
        if trial_right == target_right:
            print(f"Found P[0]! Guess = {hex(guess)} ✅")
            return guess
    print("P[0] not found in range.")
    return None

# --- التجربة دى ي دكتور---

plaintext = b"ABCDEFGH"  # 8 bytes = 64-bit
left, right = struct.unpack(">II", plaintext)
L_enc, R_enc = encrypt_block(left, right)
ciphertext = struct.pack(">II", L_enc, R_enc)

print(f"Encrypted: {ciphertext.hex()}")

# تجربة تفكيك أول عنصر في P باستخدام brute-force
found_p0 = brute_force_p0(ciphertext, plaintext)

if found_p0 is not None:
    print(f"Recovered P[0]: {hex(found_p0)}")
else:
    print("P[0] was not recovered.")
