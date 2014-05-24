# -*- coding: utf-8 -*-
"""
    tests.lib.aes_cipher_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    lib aes_cipher tests module
"""
from santa.lib import aes_cipher
import unittest, json

class AESCipherTests(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_pad(self):
        pad = aes_cipher.pad
        assert len(pad('extend_me')) == aes_cipher.BS

    def test_unpad(self):
        pad = aes_cipher.pad
        unpad = aes_cipher.unpad
        assert unpad(pad('recover_me')) == 'recover_me'

    @unittest.skip("Need to verify encoded string is url safe.")
    def test_aes_encrypt_url_safe(self):
        pass

    @unittest.skip("Need to verify encoded string is correct.")
    def test_aes_encrypt(self):
        pass

    def test_aes_encrypt_decrypt(self):
        secret = aes_cipher.pad('secret')
        AES = aes_cipher.AESCipher(secret)
        data = [ {'a': 'A', 'b': [2, 4], 'c': 3.0} ]
        data_string = json.dumps(data)
        assert AES.decrypt(AES.encrypt(data_string)) == data_string

if __name__ == '__main__':
    unittest.main()
