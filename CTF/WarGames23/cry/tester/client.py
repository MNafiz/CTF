from pwn import *

context.log_level = "warning"

for i in range(256):
    try:
        r = process(["python3", "server.py"])

        msg = b"a" + bytes([i])

        r.sendlineafter(b"> ", msg)
        print(r.recvline(0))

        r.close()
    except Exception as e:
        r.close()
        print(i)