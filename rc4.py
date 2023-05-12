def generate_key(key: str):
    encoded_key = ''.join(str(ord(c)) for c in key)
    chunks = [encoded_key[i:i + 2] for i in range(0, len(encoded_key), 2)]
    key_list = []
    while len(key_list) < 256:
        key_list.extend(chunks)
    key_list = key_list[:256]
    key_list = [int(s) for s in key_list]

    return key_list


def generate_s_array():
    s_array = []
    for i in range(0, 256):
        s_array.append(int(i))
    return s_array


def key_scheduling(key: [list]):
    s_array = generate_s_array()
    i = 0
    for j in range(0, 256):
        i = (i + s_array[j] + key[j % len(key)]) % 256
        tmp = s_array[j]
        s_array[j] = s_array[i]
        s_array[i] = tmp

    return s_array


def generation_algorithm(s_array: [list], pt: str):
    i = 0
    j = 0
    p_len = len(pt)
    key_stream = []
    while p_len > 0:
        i = (i + 1) % 256
        j = (j + s_array[i]) % 256
        tmp = s_array[j]
        s_array[j] = s_array[i]
        s_array[i] = tmp
        ks = s_array[(s_array[i] + s_array[j]) % 256]
        key_stream.append(ks)
        p_len = p_len - 1
    return key_stream


def rc4_encrypt(pt: str, key_stream: [list]):
    text = [ord(char) for char in pt]
    encrypted_text = []
    for i in range(0, len(pt)):
        encrypted_text.append(text[i] ^ key_stream[i])
    return encrypted_text


def rc4_decrypt(ct: [list], key_stream: [list]):
    decrypted_text = []
    for i in range(0, len(ct)):
        decrypted_text.append(chr(ct[i] ^ key_stream[i]))

    final_text = ''.join(decrypted_text)
    return final_text


# if __name__ == "__main__":
#     key_ = generate_key("fds")
#     plaintext = "some text to decrypt"
#
#     s_array_ = generate_s_array()
#     x = key_scheduling(key_)
#     k = generation_algorithm(x, plaintext)
#     encr = rc4_encrypt(plaintext, k)
#     print(encr)
#     print(rc4_decrypt(encr, k))
