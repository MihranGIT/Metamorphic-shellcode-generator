# POC - Generate metamorphic shellcode

[+] Python3
[+] Linux amd64

The polymorphism means the ability of an object to take on many forms. In computer science, the term polymorphism also means the ability of different objects/codes to respond in a unique way to the same functionality.

In assembly, many instructions can be replaced by others one doing the same things.
For example :
  - xor RAX, RAX is equivalent to sub RAX, RAX and this logic can be apply to all registers
  - mov al, 33 is equivalent to "mov al, 32" + "inc al" or "mov al, 20" + "add al, 13". Remember that it is hex value so 33 is equivalent to 51 in base 10.
  - NOP instruction (null instruction) can be added randomly between 2 lines of instructions
  - etc...

Many others instructions can be replaced, "dead code" can be introduced or encoding/decoding technics also.

This program simply modifies randomly some of the instructions of payload.s by instructions doing the same things.

To launch it, just clone the repository and type "python poly_shellcode.py". 
Some import may needs to be installed on your machine If you don't have it.

Output of the program :

![image](https://user-images.githubusercontent.com/91540388/157630300-6bf94abf-703c-4c81-88da-34b589170f04.png)

The payload used as POC is a simple reverse shell written in x64 for the local IP 127.0.0.1
