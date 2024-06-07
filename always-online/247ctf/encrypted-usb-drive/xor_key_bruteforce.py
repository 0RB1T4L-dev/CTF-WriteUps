from itertools import product

def find_key():
    charset = "abcdefghijklmnopqrstuvwxyz"
    
    encrypted_file = open('/mnt/bitlocker/do_not_open.png.xxx.crypt', 'rb')

    first_8_encrypted_bytes = encrypted_file.read(8)

    # Generate all possible combinations of 4 lower-case letters
    for comb in product(charset, repeat=4):
        key = comb + comb

        dec_bytes = b''

        for i in range(8):
            dec_bytes += bytes([first_8_encrypted_bytes[i] ^ ord(key[i])])

        # Compare decrypted first 8 bytes with PNG file signature
        if dec_bytes == b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
            print("Found correct key: " + ''.join(comb))
            return ''.join(comb)
        
def decrypt_file(xorkey):
    file_content = bytearray()

    xorkey = xorkey.encode()
    encrypted_file_path = '/mnt/bitlocker/do_not_open.png.xxx.crypt'
    encrypted_file = open(encrypted_file_path, 'rb')

    for i, byte in enumerate(encrypted_file.read()):
        file_content.append(byte ^ xorkey[i % len(xorkey)])

    decrypted_file_path = encrypted_file_path[:-10]

    decrypted_file = open(decrypted_file_path, 'wb')
    decrypted_file.write(file_content)
    print("Saved decrypted file to " + decrypted_file_path)

key = find_key()
decrypt_file(key)