from scapy.all import *


def decrypt(finalmessage, keys):
    messagenums = []
    for i in range(len(finalmessage)):
        messagenums.append(finalmessage[i] / keys[i])

    message = ""
    for i in range(len(messagenums)):
        message += chr(int(messagenums[i]))

    return message


packets = rdpcap("challenge.pcap")

for i in range(6, len(packets) - 1, 2):
    message = str(packets[i].load).replace("b'[", "").replace("]'", "").split(", ")
    keys = str(packets[i + 1].load).replace("b'[", "").replace("]'", "").split(", ")
    print(decrypt(list(map(int, message)), list(map(int, keys))))

# Output:
"""
hello blinkoid
hello night
how do we eliminate the msfroggers
idk i'll ask slice1
how do we eliminate the msfroggers
we can send them to the skibidi toilet
or we can deprive them of their fanum tax
slice1 is being useless
what's new
blinkoid? message back :(
oh errr... this sounds great! any more ideas
we could co-conspire with the afs
and get them to infiltrate the msfroggers
that way team lemonthink reins supreme
your a genius!
alright night
i have my own idea
let's hear it
so yk about the afs
if we send our secret code over to them
they can use it to infiltrate the afs
what's our code again?
i think it's corctf{b@53d_af_f0r_th3_w1n}
hey night did you hear my idea
you had an idea? blinkoid just told me you were being useless
what the sigma
"""
