#!/usr/bin/python

import os

for lib in ['Cryptodome', 'urllib3', 'requests']:
    try:
        __import__(lib)
    except ImportError:
        cmd = f'pip install {lib}'
        os.system(cmd)

import requests, hmac, binascii, hashlib, json, random, sys
from urllib3.util.url import Url
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES

session = requests.Session()
headers = {"User-Agent": "XiaomiPCSuite"}
ssecurity = "E5I30OwrwmlbZwB6HaQRtw=="
cookies = {'serviceToken': 'zLRA8c2eG6dVzb6SiGwM0XSbQItw0/QGW++HiqZGC52nQXGqu9+WEZIwaHQL5G40xz7fucUFNgX4AT0IzO9tn/Gu1QKN4s7Yukcf+vRzE79vBJgJKkPlPCJWu129VkcXutCqPFpNOg9JtR0d3nWeRAs3HhaLVRlzp3BP86fJxeu5ecNepEpP4+hz8ziEJoJiK+8FmSAsLNGPmLB2eAsOC6bJli5OM9ZntuAN5acVOdcc3TCSUbCWes7WNUnVZZsdv4OPGdUnUL4NE8TM8fmmS8MGE8C/gexq/kFidEAFAkXFjtXnvwp9WdRotl28YuS2', 'unlockApi_slh': 'SM8Pcw7FBMxcGEbaLbriww3U8cw=', 'unlockApi_ph': '1vGyafLHcg/9jJfslNN5LA==', 'userId': '6761184147'}
url = "unlock.update.intl.miui.com"

product = sys.argv[1]

class RetrieveEncryptData:
    def add_nonce(self):
        r = RetrieveEncryptData("/api/v2/nonce", {"r":''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid":"miui_unlocktool_client"}).run()
        self.params[b"nonce"] = r["nonce"].encode("utf-8")
        self.params[b"sid"] = b"miui_unlocktool_client"
        return self
    def __init__(self, path, params):
        self.path = path
        self.params = {k.encode("utf-8"): v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in params.items()}
    def getp(self, sep):
        return b'POST'+sep+self.path.encode("utf-8")+sep+b"&".join([k+b"="+v for k,v in self.params.items()])
    def run(self):
        self.params[b"sign"] = binascii.hexlify(hmac.digest(b'2tBeoEyJTunmWUGq7bQH2Abn0k2NhhurOaqBfyxCuLVgn4AVj7swcawe53uDUno', self.getp(b"\n"), "sha1"))
        for k, v in self.params.items():
            self.params[k] = b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt(v + (16 - len(v) % 16) * bytes([16 - len(v) % 16])))
        self.params[b"signature"] = b64encode(hashlib.sha1(self.getp(b"&")+b"&"+ssecurity.encode("utf-8")).digest())
        return json.loads(b64decode((lambda s: s[:-s[-1]])(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(b64decode(session.post(Url(scheme="https", host=url, path=self.path).url, data=self.params, headers=headers, cookies=cookies).text)))))

c = RetrieveEncryptData("/api/v2/unlock/device/clear", {"data":{"product":product}}).add_nonce().run()
cleanOrNot = c['cleanOrNot']

print("\ncleanOrNot:", cleanOrNot)
