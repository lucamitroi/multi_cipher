import math


def is_prime(value: int):
    if value > 1:
        for i in range(2, int(value / 2) + 1):
            if (value % i) == 0:
                return False
        else:
            return True
    else:
        return False


def is_primitive_root(g, p):
    if math.gcd(g, p) != 1:
        return False
    values = set()
    for i in range(1, p):
        value = pow(g, i, p)
        if value in values:
            return False
        values.add(value)
    return True


def diffie_hellman():
    prime = False
    root = False
    p = 0
    g = 0

    while not prime:
        p = input("Set a value for p (prime number): ")
        p = int(p)
        if is_prime(p) is True:
            prime = True
        else:
            print("\033[31mThe provided number is not prime\033[00m\n")

    while not root:
        g = input("Set a value for q (a primitive root modulo p): ")
        g = int(g)
        if is_primitive_root(g, p) is not False:
            root = True
        else:
            print("\033[31mThe provided number is not a primitive root modulo p\033[00m\n")

    alice = input("Provide a value for the first user (integer): ")
    alice = int(alice)

    bob = input("Provide a value for the second user (integer): ")
    bob = int(bob)

    key_name = input("Provide a name for your keys: ")
    public_key_a = pow(g, alice) % p
    key_path = "./keys/" + key_name + "_a.bin"
    with open(key_path, 'w') as f:
        f.write(str(public_key_a))

    public_key_b = pow(g, bob) % p
    key_path = "./keys/" + key_name + "_b.bin"
    with open(key_path, 'w') as f:
        f.write(str(public_key_b))

    s1 = pow(public_key_b, alice) % p
    s2 = pow(public_key_a, bob) % p

    if s1 == s2:
        print("Both users share the same shared secret:\033[93m " + str(s1) + "\n\033[00m\n")
        key_path = "./keys/" + key_name + "_shared.bin"
        with open(key_path, 'w') as f:
            f.write(str(s1))
    else:
        print("The shared secret is not the same")
