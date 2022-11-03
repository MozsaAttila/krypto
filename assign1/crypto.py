#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Mozsa Attila
SUNet: maim2059

Replace this with a description of the program.
"""

import string
import utils


# Caesar Cipher

def encrypt_caesar(plaintext):
    if len(plaintext) == 0 or (not plaintext.isupper()):
        return 'not supported format for input!'

    encode = ""
    for i in plaintext:
        if "A" <= i and i <= "Z":
            j = chr(ord(i) + 3)
            if j > 'Z':
                j = chr(ord(j) - 26)
        else:
            j = i
        encode += j

    return encode 

def encrypt_caesar_NonText(plaintext):
    encode  =  bytearray()
    for i in plaintext:
        j_num = i + 3
        if j_num > 255:
            j_num = j_num - 256
        encode+=j_num.to_bytes(1, 'big')

    return encode 

def decrypt_caesar_NonText(ciphertext):
    decode = bytearray()
    for i in ciphertext:
        j_num = i - 3
        if j_num < 0:
            j_num = j_num + 256
        decode += j_num.to_bytes(1, 'big')

    return decode

def decrypt_caesar(ciphertext):
    decode = ""
    for i in ciphertext:
        if "A" <= i and i <= "Z":
            j = chr(ord(i) - 3)
            if j < 'A':
                j = chr(ord(j) + 26)
        else:
            j = i
        decode += j

    return decode

# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    encode = ''
    k = 0
    maxl = len(keyword)
    for i in plaintext:
        j = chr(ord(i) + ord(keyword[k]) - ord('A'))
        if j > 'Z':
            j = chr(ord(j) - 26)
        encode += j
        k +=1
        if(k>=maxl):
            k = 0
    
    return encode

def decrypt_vigenere(ciphertext, keyword):
    decode = ''
    k = 0
    maxl = len(keyword)
    for i in ciphertext:
        j = chr(ord(i) - ord(keyword[k]) + ord('A'))
        if j < 'A':
            j = chr(ord(j) + 26)
        decode += j
        k +=1
        if(k>=maxl):
            k = 0
    
    return decode

from langdetect import detect
def attack_vigenere(ciphertext):
    f = open('D:\\UBB\\V.felev\\kripto\\words')
    words = f.readlines()
    f.close()
    for word in words:
        word2 = word.split('\'')[0]
        print(word2)
        decrypted = decrypt_vigenere(ciphertext,word2)
        #if detect(decrypted) == 'en':
            #print(decrypted)

#f = open('D:\\UBB\\V.felev\\kripto\\lab1\\krypto\\assign1\\not_a_secret_message.txt')
#text = f.readlines()[-1]
#attack_vigenere(text)

#scytale cipher

def encrypt_scytal(plaintext, circumference):
    encode = ''
    l = len(plaintext)
    for i in range(0,circumference):
        j = i
        while j < l:
            encode += plaintext[j]
            j += circumference
    
    return encode

def decrypt_scytal(ciphertext, circumference):
    decode = ''
    l = len(ciphertext)
    div = l//circumference
    mod = l%circumference
    for i in range(0,div):
        j = i
        k = 0
        while j < l:
            decode += ciphertext[j]
            if k < mod:
                j += div + 1
            else:
                j += div
            k += 1
    
    i = div
    for j in range(0,mod):
        decode += ciphertext[i]
        i += div
    
    return decode

#railfence cipher

def encrypt_railfence(plaintext, num_rails):
    encode = ''
    l = len(plaintext)
    matrix = [['\n' for _ in range(l)] for _ in range(num_rails)]

    down = -1
    r, c = 0, 0

    for i in range(l):
        if r == 0 or r == num_rails - 1:
            down *= -1
        matrix[r][c] = plaintext[i]
        c += 1
        r += down

    for i in range(num_rails):
        for j in range(c):
            if matrix[i][j] != '\n':
                encode += matrix[i][j]
    
    return encode   

def decrypt_railfence(ciphertext, num_rails):
    decode = ''
    l = len(ciphertext)
    
    matrix = [['\n' for _ in range(l)] for _ in range(num_rails)]

    down = -1
    r, c = 0, 0

    for i in range(l):
        if r == 0 or r == num_rails - 1:
            down *= -1
        matrix[r][c] = 'a'
        c += 1
        r += down

    k = 0
    for i in range(num_rails):
        for j in range(c):
            if matrix[i][j] == 'a':
                matrix[i][j] = ciphertext[k]
                k += 1

    down = -1
    r, c = 0, 0
    for i in range(l):
        if r == 0 or r == num_rails - 1:
            down *= -1
        decode += matrix[r][c]
        c += 1
        r += down

    return decode


# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here

