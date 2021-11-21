from RSA import *
from SHA256 import *

class Signature:
    def __init__(self, text, n=None, e=None):
        self.text = text
        if(n != None):
            self.n = n
        if(e != None):
            self.e = e

    def signFile(self):
        signature = int(sha256(self.text), 16)
        rsa = RSA(str(signature))
        signature = rsa.encryptNumber()
        signedText = self.text + "\n\n**Digital Signature**" + signature + "**Digital Signature**"

        f_signed = open('signedText.txt', 'w')
        f_signed.write(signedText)
        f_signed.close()

        return signedText

    def validateSign(self):
        splittedText = self.text.split("**Digital Signature**")
        textFile = splittedText[0][:-2]
        while(textFile[-1] == '\n' or textFile[-1] == '\r'):
            textFile = textFile[:-1]
        signature = splittedText[1]

        hashedText = int(sha256(textFile), 16) % self.n
        processedSignature = (int(signature, 16) ** self.e) % self.n

        if(hashedText == processedSignature):
            return True
        else:
            return False

# # signing
# text = "hello world"
# sign1 = Signature(text)
# print(text)
# signedText = sign1.signFile()
# print(signedText)

# # validating
# print("======VALIDATING======")
# f = open("publicKey.pub", "r")
# key = f.read()
# pubN,pubE = key.replace(" ","").split(",")
# pubN,pubE = int(pubN), int(pubE)
# f.close()
# sign2 = Signature(signedText, n=pubN, e=pubE)
# valid = sign2.validateSign()

# if(valid):
#     print("Valid!")
# else:
#     print("Invalid!")