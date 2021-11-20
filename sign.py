from RSA import *
from SHA256 import *

text = "Pada wisuda sarjana baru ITB, ternyata ada seorang wisudawan yang paling muda. Umurnya baru 19 tahum. Ini berarti dia masuk ITB pada umur 15 tahum. Zaman sekarang banyak sarjana masih berusia muda belia. Mungkin masuk sekolah pada usia dini dan mengikuti kelas akselerasi pada tingkatan SD, SMP, dan SMA. Masuk SD umur 6 tahun dan ikut kelas aksel sehingga selesai dalam waktu lima tahun pada umur 11. SMP diselesaikan dalam waktu dua tahun dan SMA dalam waktu dua tahun, sehingga lulus SMA pada umur 15 tahun. Kuliah di ITB selama empat tahun sehingga wajar saja menjadi sarjana pada umur 19 tahun."
text2 = "hello world"
print(sha256(text2))
print(int(sha256(text2), 16))

s = int(sha256(text2), 16)

rsa = RSA(str(s))
signature = rsa.encryptNumber()
print(signature)

signedText = text2 + "\n\n**Digital Signature**" + signature + "**Digital Signature**"
print(signedText)

# Validating
print("===========VALIDATING===========")
receivedSplit = signedText.split("**Digital Signature**")
receivedText = receivedSplit[0][:-2]
receivedSignature = receivedSplit[1]
print(receivedText)
print(receivedSignature)

f = open("publicKey.pub", "r")
key = f.read()
n,e = key.replace(" ","").split(",")
n,e = int(n), int(e)
f.close()

print("###############")
print("HASHED MESSAGE:")
hashedReceivedText = int(sha256(receivedText), 16) % n
print(hashedReceivedText)
print("###############")
print("VALIDATING SIGNATURE:")
processedReceivedSignature = (int(receivedSignature, 16) ** e) % n
print(processedReceivedSignature)
print("###############")
if(hashedReceivedText == processedReceivedSignature):
    print("SIGNATURE VALID!")
else:
    print("SIGNATURE NOT VALID!")