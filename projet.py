#!/usr/bin/python3
import random
import sys
from pwn import *
import os
from colorama import Fore, Back, Style


context(os="linux", arch="amd64", log_level="error")

def code_changer():
    AssemblyCode = open("payload", 'r')
    new_payload = open("new_payload.s", 'w+')
    Lines = AssemblyCode.readlines()
    for line in Lines:
        stripped_line = line.strip()
        if "xor rdx, rdx" in line:
            n = random.randint(0,1)
            if n == 1:
                line = stripped_line.replace("xor rdx, rdx", "sub rdx, rdx \n")
        if "xor rax, rax" in line:
            n = random.randint(0,1)
            if n == 1:
                line = stripped_line.replace("xor rax, rax", "sub rax, rax \n")
        if "xor rbx, rbx" in line:
            n = random.randint(0,1)
            if n == 1:
                line = stripped_line.replace("xor rbx, rbx", "sub rbx, rbx \n")
        if "xor rdi, rdi" in line:
            n = random.randint(0,1)
            if n == 1:
                line = stripped_line.replace("xor rdi, rdi", "sub rdi, rdi \n")
        if "xor rcx, rcx" in line:
            n = random.randint(0,1)
            if n == 1:
                line = stripped_line.replace("xor rcx, rcx", "sub rcx, rcx \n")
        if "xor rsi, rsi" in line:
            n = random.randint(0,1)
            if n == 1:
                line = stripped_line.replace("xor rsi, rsi", "sub rsi, rsi \n")
        new_payload.write(stripped_line)


def check_nullbyte():
    file = ELF("payload")
    shellcode = file.section(".text")
    nullbyte = False
    print("[+] Shellcode : ", shellcode.hex())
    for i in shellcode:
            if i == 0:
                nullbyte = True
    if nullbyte == True:
        print(Fore.RED + "[+] Payload original: %d bytes - Found NULL bytes" % len(shellcode))
        print(Fore.RED + "[+] Please submit a valid shellcode")
        print(Style.RESET_ALL)
    if nullbyte == False:
        print(Fore.GREEN + "[+] Payload original : %d bytes - No NULL bytes" % len(shellcode))
        print(Style.RESET_ALL)
        code_changer()

check_nullbyte()
