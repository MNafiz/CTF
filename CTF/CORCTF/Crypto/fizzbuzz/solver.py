from pwn import *
import re

context.log_level = "warning"

for i in range(10):
    print(i)
    try:
        r = remote("be.ax",31100)

        for i in range(3):
            exec(r.recvline(0))

        guess1 = pow(7,-1,n)

        r.sendlineafter(b"> ", str(guess1).encode())

        payload1 = int(r.recvline(0).decode())

        guess2 = (7 * ct) % n

        r.sendlineafter(b"> ", str(guess2).encode())

        payload2 = int(r.recvline(0).decode())

        m = (payload1*payload2) % n

        flag = bytes.fromhex(hex(m)[2:])


        r.close()
        break
    except:
        r.close()

flag = re.findall(b"corctf{.*}",flag)[0]
print(flag)