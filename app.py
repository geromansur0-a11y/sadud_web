from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "sadud_secret"

def db():
    return sqlite3.connect("sadud.db")

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        c = db().cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        if c.fetchone():
            session["login"] = True
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("login"):
        return redirect("/")
    c = db().cursor()
    barang = c.execute("SELECT * FROM barang").fetchall()
    return render_template("dashboard.html", data=barang)

@app.route("/barang", methods=["GET","POST"])
def barang():
    if request.method == "POST":
        db().cursor().execute(
            "INSERT INTO barang(nama,harga,stok) VALUES (?,?,?)",
            (request.form["nama"], request.form["harga"], request.form["stok"])
        )
        db().commit()
    data = db().cursor().execute("SELECT * FROM barang").fetchall()
    return render_template("barang.html", data=data)

@app.route("/penjualan", methods=["GET","POST"])
def penjualan():
    c = db().cursor()
    barang = c.execute("SELECT * FROM barang").fetchall()

    if request.method == "POST":
        idb = request.form["barang"]
        qty = int(request.form["qty"])
        b = c.execute("SELECT harga FROM barang WHERE id=?", (idb,)).fetchone()
        total = qty * b[0]

        c.execute("INSERT INTO penjualan(barang_id,qty,total,tanggal) VALUES (?,?,?,date('now'))",
                  (idb,qty,total))
        c.execute("UPDATE barang SET stok=stok-? WHERE id=?", (qty,idb))
        db().commit()

    return render_template("penjualan.html", barang=barang)

@app.route("/laporan")
def laporan():
    c = db().cursor()
    jual = c.execute("SELECT SUM(total) FROM penjualan").fetchone()[0] or 0
    return render_template("laporan.html", total=jual)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run(host="0.0.0.0", port=5000, debug=True)
