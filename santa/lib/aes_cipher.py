# -*- coding: utf-8 -*-
"""
    santa.lib.aes_cipher.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    'aes_cipher' lib for AES encryption/decryption

    :copyright: (c) 2013 by Chung-Yi Chi
    :license:
"""

# http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
from Crypto import Random
from Crypto.Cipher import AES
import base64, json

BS = 16
def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
def unpad(s):
    return s[0:-ord(s[-1])]

class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.urlsafe_b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.urlsafe_b64decode(enc)
        iv = enc[:16]
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

if __name__ == '__main__':
    aes = AESCipher(pad('secret'))
    data = [ { 'a': 'A', 'b': (2, 4), 'c': 3.0 } ]
    data_str = json.dumps(data)
    enc = aes.encrypt(data_str)
    print "raw: " + data_str
    print "enc: " + enc
    print "dec: " + aes.decrypt(enc)
