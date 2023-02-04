import hashlib

from jpype import JClass

from core import config
# from core.SocketClient import SocketClient

instanct = None
encryptKey = "weichats"


def getInstance():
    global instanct
    if not isinstance(instanct, Base64):
        instanct = Base64()
    return instanct


# def destoryInstance():
#     global instanct
#     instanct.disConnect()
#     instanct = None


class Base64:
    def __init__(self):
        self.XXTEA = JClass("XXTEA")
        self.AES = JClass("AES")
        # self.conf = config.getInstance()
        # host = self.conf.get_value_by_key('main', 'crypt_server_host')
        # port = self.conf.get_value_by_key('main', 'crypt_server_port')
        # self.socketClient = SocketClient(host, int(port))

    # def disConnect(self):
    #     self.socketClient.close()

    def decrypt(self, decryptstr):
        return str(self.XXTEA.decryptBase64StringToString(decryptstr, encryptKey))
        # data = {
        #     "action": "decrypt",
        #     "data": str,
        #     "seed": encryptKey
        # }
        # return self.socketClient.sendMsg(json.dumps(data))

    def encrypt(self, encryptstr):
        return str(self.XXTEA.encryptToBase64String(encryptstr, encryptKey))
        # data = {
        #     "action": "encrypt",
        #     "data": str,
        #     "seed": encryptKey
        # }
        # return self.socketClient.sendMsg(json.dumps(data))

    def AES_decrypt(self, encryptstr):
        token = config.getInstance().get_XHL_token()
        parmStr = token.encode("utf-8")
        myMd5 = hashlib.md5()
        myMd5.update(parmStr)
        myMd5_Digest = myMd5.hexdigest()
        return str(self.AES.aesdecrypt(encryptstr, myMd5_Digest))
