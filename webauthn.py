from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity
import sqlite3

rp = PublicKeyCredentialRpEntity("sadud.app", "SADUD")
server = Fido2Server(rp)

def db():
    return sqlite3.connect("sadud.db")

def get_creds(username):
    c = db().cursor()
    rows = c.execute(
        "SELECT credential_id, public_key FROM webauthn_credentials WHERE username=?",
        (username,)
    ).fetchall()
    return rows

def save_cred(username, cred_id, public_key):
    c = db().cursor()
    c.execute(
        "INSERT INTO webauthn_credentials(username,credential_id,public_key) VALUES (?,?,?)",
        CREATE TABLE webauthn_credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    credential_id TEXT,
    public_key BLOB
);

      (username, cred_id, public_key)
    )
    db().commit()
