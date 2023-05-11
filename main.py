from aes import *
import os


def slice_string(s):
    return [s[i:i+16] for i in range(0, len(s), 16)]


if __name__ == "__main__":
    run = True

    while run:
        print("Which algorithm do you want to use?")
        print("1. Advanced Encryption Standard")
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
                text = input("Enter the text that you want to encrypt: ")
                print("\nThe encrypted text is: ")
                sliced_list = slice_string(text)
                for list_element in sliced_list:
                    plaintext = bytearray(list_element.encode())
                    if len(plaintext) % 16 != 0:
                        plaintext.extend(b'\0' * (16 - len(plaintext) % 16))
                    key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f')
                    ciphertext = aes_encryption(plaintext, key)
                    print("\033[93m" + str(ciphertext) + "\n\033[00m")
        elif value == '0':
            run = False
