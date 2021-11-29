import random
import socket
max_PrimLength = 1000000000000

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num ** 0.5) + 2, 2):
        if num % n == 0:
            return False
    return True

def generateRandomPrim():
    while (1):
        ranPrime = random.randint(0, max_PrimLength)
        if is_prime(ranPrime):
            return ranPrime


def generate_keyPairs():
    p = generateRandomPrim()
    q = generateRandomPrim()

    n = p * q
    #print("n ", n)
    '''phi(n) = phi(p)*phi(q)'''
    phi = (p - 1) * (q - 1)
    #print("phi ", phi)

    '''choose e coprime to n and 1 > e > phi'''
    e = random.randint(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)

    #print("e=", e, " ", "phi=", phi)
    '''d[1] = modular inverse of e and phi'''
    d = egcd(e, phi)[1]

    '''make sure d is positive'''
    d = d % phi
    if (d < 0):
        d += phi

    return ((e, n), (d, n))


# generate for client & Server private and public keys.
public_key_client, private_key_client = generate_keyPairs()
public_key_server, private_key_server = generate_keyPairs()


print("public_key_client = ",public_key_client)
print("private_key_client = ",private_key_client)

print("public_key_server = ",public_key_server)
print("private_key_server = ",private_key_server)