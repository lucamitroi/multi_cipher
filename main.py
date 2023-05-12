from aes import aes_encryption, aes_decryption
from diffie_hellman import diffie_hellman
import os
import secrets
import base64
from random_word import RandomWords
from rc4 import *


def slice_string(s: str, number: int):
    return [s[i:i+number] for i in range(0, len(s), number)]


if __name__ == "__main__":
    run = True

    while run:
        print("\033[34mWhich algorithm do you want to use?\n\033[00m")
        print("1. Advanced Encryption Standard")
        print("2. Rivest Cipher 4")
        print("3. Diffie-Hellman")
        print("0. Exit\n")

        value = input("Please enter a number: ")
        print()
        if value == '1':
            print("\033[34mWhat do you want to do?\033[00m")
            print("1. Encrypt")
            print("2. Decrypt\n")

            value2 = input("Please enter a number: ")
            if value2 == '1':
                print()
                encrypted_text = ''
                text = input("Enter the text that you want to encrypt: ")
                key_name = input("Enter the name of the key: ")
                key_path = "./keys/" + key_name + ".bin"
                key = secrets.token_bytes(16)
                sliced_list = slice_string(text, 16)
                for list_element in sliced_list:
                    plaintext = bytearray(list_element.encode())
                    if len(plaintext) % 16 != 0:
                        plaintext.extend(b'\0' * (16 - len(plaintext) % 16))
                    ciphertext = aes_encryption(plaintext, key)
                    encoded_bytes = base64.b64encode(ciphertext)
                    encrypted_text = encrypted_text + str(encoded_bytes)[2:-1]

                message_bytes = encrypted_text.encode('ascii')
                base64_bytes = base64.b64encode(message_bytes)
                encrypted_text = base64_bytes.decode('ascii')
                print("\nThe encrypted text is: \033[93m" + encrypted_text + "\n\033[00m")

                encoded_key = base64.b64encode(key)
                with open(key_path, 'w') as f:
                    f.write(str(encoded_key)[2:-1])

            elif value2 == '2':
                print()
                decrypted_text = ''
                text = input("Enter the text that you want to decrypt: ")
                base64_bytes = text.encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                text = message_bytes.decode('ascii')
                key_path = input("Provide the path to the key: ")
                if not os.path.isfile(key_path):
                    print(f"File '{key_path}' not found\n")
                else:
                    with open(key_path, 'r') as file:
                        key = file.read()
                        key = base64.b64decode(key)
                    sliced_list = slice_string(text, 24)
                    for list_element in sliced_list:
                        decoded_bytes = base64.b64decode(list_element)
                        recovered_plaintext = aes_decryption(decoded_bytes, key)
                        decrypted_text = decrypted_text + str(recovered_plaintext)[2:-1]

                    decrypted_text = decrypted_text.replace("\\x00", "")
                    print("The decrypted text is: \033[93m" + decrypted_text + "\n\033[00m\n")

            else:
                print("Not a valid option")
        elif value == '2':
            print("\033[34mWhat do you want to do?\033[00m")
            print("1. Encrypt")
            print("2. Decrypt\n")

            value2 = input("Please enter a number: ")
            if value2 == '1':
                print()
                text = input("Enter the text that you want to encrypt: ")
                key_name = input("Enter the name of the key: ")
                key_path = "./keys/" + key_name + ".bin"
                r = RandomWords()
                key = generate_key(r.get_random_word())
                ks = key_scheduling(key)
                final_key = generation_algorithm(ks, text)
                print(final_key)
                with open(key_path, 'w') as f:
                    f.write(str(final_key)[1:-1])
                encrypted_text = rc4_encrypt(text, final_key)
                print("\nThe encrypted text is: \033[93m" + str(encrypted_text) + "\n\033[00m")
            elif value2 == '2':
                print()
                text = input("Enter the text that you want to decrypt: ")
                text = text.split(',')
                text = [int(s) for s in text]
                key_path = input("Provide the path to the key: ")
                if not os.path.isfile(key_path):
                    print(f"File '{key_path}' not found\n")
                else:
                    with open(key_path, 'r') as file:
                        key = file.read()
                    key = key.split(',')
                    key = [int(s) for s in key]
                    decrypted_text = rc4_decrypt(text, key)
                    print("The decrypted text is: \033[93m" + decrypted_text + "\n\033[00m")

        elif value == '3':
            diffie_hellman()
        elif value == '0':
            run = False
