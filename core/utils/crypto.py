import jwt
import yaml
import os
import base64
import hashlib
from django.conf import settings
from Crypto.Cipher import DES3
from Crypto.Hash import SHA256


class ADACrypto:

    def encrypt_file(file, fileOut):

        chunk_size=8192
        hex_key=settings.SECRET_KEY[:24].encode()

        #Create the cipher to decrypt the data
        des3 = DES3.new(hex_key, DES3.MODE_ECB)

        with open(file, 'r') as in_file:
            with open(fileOut, 'wb') as out_file:
                while True:
                    chunk = in_file.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)
                    chung_bytes=chunk.encode()
                    out_file.write(des3.encrypt(chung_bytes))

    def decrypt_file(file, out_filename=None):

        chunk_size=8192
        hex_key=settings.SECRET_KEY[:24].encode()

        #Create the cipher to decrypt the data
        des3 = DES3.new(hex_key, DES3.MODE_ECB)

        if out_filename == None:
            output=''
            with open(file, 'rb') as in_file:
                while True:
                    chunk = in_file.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    output=output+des3.decrypt(chunk).decode('utf-8')
            return output
        else:
            with open(file, 'rb') as in_file:
                with open(out_filename, 'w') as out_file:
                    while True:
                        chunk = in_file.read(chunk_size)
                        if len(chunk) == 0:
                            break
                        out_file.write(des3.decrypt(chunk).decode('utf-8'))

