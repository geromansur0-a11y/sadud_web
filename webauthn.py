from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity
from fido2.utils import websafe_encode, websafe_decode

rp = PublicKeyCredentialRpEntity("sadud.local", "SADUD")
server = Fido2Server(rp)

# Simpan credential di DB (contoh memory)
credentials = {}
