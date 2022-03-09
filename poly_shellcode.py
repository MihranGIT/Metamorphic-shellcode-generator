#!/usr/bin/python3
import random
import sys
from pwn import *
import os
from colorama import Fore, Back, Style

context(os="linux", arch="amd64", log_level="error")

def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

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
        print("[+] Payload original : payload.s")
        print("[+] Payload assemblé et linké : payload")
        print(Fore.GREEN + "[+] Taille : %d bytes - No NULL bytes" % len(shellcode))
        print(Style.RESET_ALL)
        code_changer()
        new_payload()
        clean()

def assembler_payload():
    os.system("nasm -f elf64 payload.s")
    os.system("ld payload.o -o payload")

def code_changer():
    AssemblyCode = open("payload.s", 'r')
    new_payload = open("new_payload.s", 'w+')
    Lines = AssemblyCode.readlines()
    i=0
    for line in Lines:
        i=i+1
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
        if "mov al, 33" in line:
            n = random.randint(0,1)
            if n == 1:
                n = random.randint(0,50)
                line = stripped_line.replace("mov al, 33", "mov al, " +  hex(n) + "\n")
                reste = 51 - n
                Lines.insert((i), "add al, " + hex(reste) +  "\n")
        new_payload.write(line)
    new_payload.close()
    AssemblyCode.close()

def new_payload():
    os.system("nasm -f elf64 new_payload.s")
    os.system("ld new_payload.o -o new_payload")
    file = ELF("new_payload")
    shellcode = file.section(".text")
    print("[+] Code assembleur du nouveau shellcode : new_payload.s")
    print("[+] Nouveau payload compilé et linké : new_payload")
    print("[+] New shellcode : ", shellcode.hex())
    print("[+] Taille : %d bytes - No NULL bytes" % len(shellcode))

def clean():
    os.system("rm payload.o")
    os.system("rm new_payload.o")

print("[+] Shellcode generator - amd64 - x86 \n")
assembler_payload()
check_nullbyte()
