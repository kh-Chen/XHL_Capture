import socket


class SocketClient:
    def __init__(self, host, port):
        self.sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockClient.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.sockClient.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        self.sockClient.connect((host, port))

    def sendMsg(self, str):
        msg = str.encode('utf-8')
        slen = len(msg).to_bytes(length=4, byteorder='big', signed=True)
        self.sockClient.sendall(slen)
        self.sockClient.sendall(msg)
        b_reclen = self.sockClient.recv(4)
        reclen = int().from_bytes(b_reclen, byteorder='big', signed=True)
        return self.sockClient.recv(reclen).decode('utf-8')

    def close(self):
        bye = "bye"
        bye = bye.encode('utf-8')
        byelen = len(bye).to_bytes(length=4, byteorder='big', signed=True)
        self.sockClient.sendall(byelen)
        self.sockClient.sendall(bye)
