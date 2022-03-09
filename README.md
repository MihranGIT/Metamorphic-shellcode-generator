# POC - Generate polymorphic shellcode

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

Screenshots :
![image](https://user-images.githubusercontent.com/91540388/157424416-9ab21f5e-00ab-4a52-b687-cbe8a9d691a2.png)

