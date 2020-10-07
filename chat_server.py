from socket import *
import os
ADDR = ('0.0.0.0', 8888)
usr = {}


def do_login(s, name, addr):
    if name in usr:
        s.sendto("该用户已存在".encode(), addr)
        return

    s.sendto(b'OK', addr)

    # 通知其它人
    msg = "欢迎%s进入聊天室" % name
    for i in usr:
        s.sendto(msg.encode(), usr[i])
    # 将用户加入
    usr[name] = addr


# 聊天
def do_chat(s, name, text):
    msg = "%s : %s" % (name, text)
    for i in usr:
        if i != name:
            s.sendto(msg.encode(), usr[i])


# 退出
def do_quit(s, name):
    msg = "%s退出了聊天室" % name
    for i in usr:
        if i != name:
            s.sendto(msg.encode(), usr[i])
        else:
            s.sendto(b'EXIT', usr[i])
    # 将用户删除
    del usr[name]


def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split()
        name = ' '.join(msg[1:])
        if msg[0] == 'L':
            do_login(s, name, addr)
        elif msg[0] == 'C':
            text = ' '.join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == 'Q':
            if name not in usr:
                s.sendto(b'EXIT', ADDR)
                continue
            do_quit(s, name)


def main():
    # 套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    # 请求处理
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息:")
            msg = "C 管理员消息 " + msg
            s.sendto(msg.encode(), ADDR)
    else:
        do_request(s)  # 处理客户端请求


if __name__ == "__main__":
    main()
