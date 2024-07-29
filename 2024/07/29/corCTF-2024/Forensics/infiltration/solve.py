
from pwn import *
conn = remote("be.ax", 32222)
answers = [
    "slice1",
    "lemon-squeezer",
    "83",
    "1721946080",
    "notabackdoor",
    "Administrators",
]
for answer in answers:
    conn.sendline(answer.encode("ascii"))
    print(conn.recv().decode("ascii"))
conn.close()
