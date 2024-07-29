import random
from scapy.all import *
import csv

sources, destinations, messages = [], [], []

# 打开名为chatlogs.csv的文件，读取其中的内容，并将源地址、目的地址和消息分别存储在sources、destinations和messages列表中
with open("chatlogs.csv", mode="r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        sources.append(row[0])
        destinations.append(row[1])
        messages.append(row[2])


# 定义一个加密函数，将消息转换为数字，并生成随机密钥进行加密
def encrypt(message):
    messagenums = []
    for character in message:
        messagenums.append(ord(character))
    keys = []
    for i in range(len(messagenums)):
        keys.append(random.randint(10, 100))

    finalmessage = []
    for i in range(len(messagenums)):
        finalmessage.append(messagenums[i] * keys[i])

    return keys, finalmessage





# 遍历消息列表，对每条消息进行加密并发送
for i in range(len(messages)):
    finalmessage, keys = encrypt(messages[i])
    print(finalmessage, keys)
    # 构造两个数据包，分别包含加密后的消息和密钥，并发送出去
    packet1 = (
        IP(src=sources[i], dst=destinations[i])
        / TCP(dport=80)
        / Raw(load=str(finalmessage))
    )
    send(packet1)
    packet2 = (
        IP(src=sources[i], dst=destinations[i]) / TCP(dport=80) / Raw(load=str(keys))
    )
    send(packet2)
