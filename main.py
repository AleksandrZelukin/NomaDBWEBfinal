# https://metanit.com/sql/sqlite/3.1.php
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

db = sqlite3.connect('noma.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS nomnieks(
    id_nomnieks INTEGER PRIMARY KEY AUTOINCREMENT,
    "vards" TEXT, 
    "uzvards" TEXT, 
    "talrunis" TEXT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS instrumenti (
    id_instruments INTEGER PRIMARY KEY AUTOINCREMENT,
    instruments TEXT,
    marka TEXT,
    cena TEXT
 )""")

sql.execute("""CREATE TABLE IF NOT EXISTS noma (
    id_noma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_nomnieks INTEGER,
    id_instruments INTEGER,
    data_in TEXT,
    data_out TEXT,
    FOREIGN KEY("id_instruments") REFERENCES "Instrumenti"("id_instruments"),
    FOREIGN KEY("id_nomnieks") REFERENCES "Nomnieks"("id_nomnieks")
 )""")
db.commit()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/nomnieks', methods=['POST', 'GET'])
def nomnieki():
    if request.method == "POST":
        vards = request.form["vards"]
        uzvards = request.form["uzvards"]
        talrunis = request.form["talrunis"]
        a = [vards,uzvards,talrunis]
        db = sqlite3.connect('noma.db')
        sql = db.cursor()
        sql.execute("INSERT INTO nomnieks(vards,uzvards,talrunis) VALUES(?,?,?)",a)
        db.commit()
    return render_template('nomnieks.html')

@app.route('/instrumenti', methods=['POST', 'GET'])
def instrumenti():
    if request.method == "POST":
        instruments = request.form["instruments"]
        marka = request.form["marka"]
        cena = request.form["cena"]
        b = [instruments,marka,cena]
        db = sqlite3.connect('noma.db')
        sql = db.cursor()
        sql.execute("INSERT INTO instrumenti(instruments,marka,cena) VALUES(?,?,?)",b)
        db.commit()
        sql.execute("SELECT * FROM instrumenti")
        rez = sql.fetchall()
        db.close()
    return render_template('instrumenti.html')
    return render_template('instrumenti.html',rows = rez)

@app.route('/noma', methods=['POST', 'GET'])
def noma():
  if request.method == "POST":
      id_nomnieks = request.form["id_nomnieks"]
      id_instruments = request.form["id_instruments"]
      data_in = request.form["data_in"]
      data_out = request.form["data_out"]
      c = [id_nomnieks,id_instruments, data_in,data_out]
      db = sqlite3.connect('noma.db')
      sql = db.cursor()
      sql.execute("INSERT INTO noma (id_nomnieks,id_instruments, data_in,data_out)VALUES(?,?,?,?)",c)
      db.commit()
      db.close()
  return render_template("noma.html")

@app.route('/kopa', methods=['POST', 'GET'])
def kopa():
  db = sqlite3.connect('noma.db')
  sql = db.cursor()
  sql.execute("SELECT vards,uzvards,instruments,marka,data_in,data_out FROM noma JOIN nomnieks ON nomnieks.id_nomnieks = noma.id_nomnieks JOIN instrumenti ON instrumenti.id_instruments = noma.id_instruments")
  records = sql.fetchall()
  print(records)
  return render_template("kopa.html", rows = records)

@app.route('/nomn_kopa', methods=['POST', 'GET'])
def nomn_kopa():
  db = sqlite3.connect('noma.db')
  sql = db.cursor()
  sql.execute("SELECT * FROM nomnieks")
  records = sql.fetchall()
  print(records)
  return render_template("visi_nomnieki.html", rows = records)

@app.route('/inst_kopa', methods=['POST', 'GET'])
def inst_kopa():
  db = sqlite3.connect('noma.db')
  sql = db.cursor()
  sql.execute("SELECT * FROM instrumenti")
  records = sql.fetchall()
  print(records)
  return render_template("visi_instrumenti.html", rows = records)

@app.route('/nomn_dzest', methods=['POST', 'GET'])
def nomn_dzest():
  if request.method == "POST":
    id_nomnieks = request.form["id_nomnieks"]
    dzest = [id_nomnieks]
    db = sqlite3.connect('noma.db')
    sql = db.cursor()
    sql.execute("DELETE FROM nomnieks WHERE id_nomnieks = ?",id_nomnieks)
    db.commit()
  return render_template("nomnieks_dzest.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0',port="8080",debug=True)


# records = sql.fetchall()
#   print(records)