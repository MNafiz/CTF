#!/usr/bin/python3
import random
import os
from Crypto.Util.number import *

class ECG:
    def __init__(self):
        self.m = getPrime(64)
        self.a = getPrime(64) % self.m
        self.c = getPrime(64) % self.m
        self.state = getPrime(64) % self.m
    def next(self):
        self.state = (pow(self.a, self.state, self.m) + self.c) % self.m
        return self.state

def enc(msg):
    msg = bytes_to_long(msg)
    random.seed(ecg.next())
    return random.getrandbits(1024) ^ msg

ecg = ECG()
flag = open('flag.txt', 'rb').read()

enc_flag = enc(flag)

points = 6
while points > 0:
    print("1. Leak a")
    print("2. Leak c")
    print("3. Leak m")
    print("4. Leak next state")
    print("5. Leak flag")
    print("6. Exit")
    choice = int(input(">> "))
    if choice == 1:
        points -= 2
        print("a = {}".format(ecg.a))
    elif choice == 2:
        points -= 2
        print("c = {}".format(ecg.c))
    elif choice == 3:
        points -= 2
        print("m = {}".format(ecg.m))
    elif choice == 4:
        points -= 1
        print("next state = {}".format(ecg.next()))
    elif choice == 5:
        points -= 1
        print("enc(flag) = {}".format(enc_flag))
    elif choice == 6:
        break
print("Enough!")