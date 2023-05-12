from aes import aes_encryption, aes_decryption
from diffie_hellman import diffie_hellman
import os
import secrets
import base64


def slice_string(s: str, number: int):
    return [s[i:i+number] for i in range(0, len(s), number)]


if __name__ == "__main__":
    run = True

    while run:
        print("Which algorithm do you want to use?")
        print("1. Advanced Encryption Standard")
        print("3. Diffie-Hellman")
        print("0. Exit\n")

        value = input("Please enter a number: ")
        print()
        if value == '1':
            print("What do you want to do?")
            print("1. Encrypt")
            print("2. Decrypt\n")

            value2 = input("Please enter a number: ")
            if value2 == '1':
                print()
                encrypted_text = ''
                key_name = input("Enter the name of the key: ")
                key_path = "./keys/" + key_name + ".bin"
                key = secrets.token_bytes(16)
                text = input("Enter the text that you want to encrypt: ")
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
        elif value == '3':
            diffie_hellman()
        elif value == '0':
            run = False
