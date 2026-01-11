from flask import Flask, render_template, request, session, redirect, jsonify
from webauthn import server, credentials
import os

app = Flask(__name__)
app.secret_key = "sadud-secret"

@app.route("/register")
def register():
    return render_template("register_finger.html")

@app.route("/register/begin")
def register_begin():
    user = {
        "id": os.urandom(16),
        "name": "admin",
        "displayName": "Admin SADUD"
    }
    registration_data, state = server.register_begin(
        user,
        credentials.get("admin", []),
        user_verification="required"
    )
    session["state"] = state
    return jsonify(registration_data)

@app.route("/register/complete", methods=["POST"])
def register_complete():
    data = request.get_json()
    auth_data = server.register_complete(
        session["state"],
        data
    )
    credentials.setdefault("admin", []).append(auth_data.credential_data)
    return {"success": True}

@app.route("/login/finger/begin")
def login_begin():
    auth_data, state = server.authenticate_begin(
        credentials.get("admin", [])
    )
    session["state"] = state
    return jsonify(auth_data)

@app.route("/login/finger/complete", methods=["POST"])
def login_complete():
    data = request.get_json()
    server.authenticate_complete(
        session["state"],
        credentials.get("admin", []),
        data
    )
    session["login"] = True
    return {"success": True}

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("login"):
        return redirect("/")
    return "LOGIN BERHASIL (Fingerprint)"
