from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

db = sqlite3.connect('noma.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS nomnieks(
    id_nomnieks TEXT PRIMARY KEY,
    "vards" TEXT, 
    "uzvards" TEXT, 
    "talrunis" TEXT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS instrumenti (
    id_instruments TEXT PRIMARY KEY,
    instruments TEXT,
    data TEXT,
    cena TEXT
 )""")

sql.execute("""CREATE TABLE IF NOT EXISTS noma (
    id_noma TEXT PRIMARY KEY,
    id_nomnieks TEXT,
    id_instruments TEXT,
    FOREIGN KEY("id_instruments") REFERENCES "Instrumenti"("id_instruments"),
    FOREIGN KEY("id_nomnieks") REFERENCES "Nomnieks"("id_nomnieks")
 )""")
db.commit()


@app.route('/')
def index():
  db = sqlite3.connect('noma.db')
  sql = db.cursor()
  sql.execute('SELECT * FROM instrumenti')
  inst_all = sql.fetchall()
  return render_template('index.html',rows=inst_all)

@app.route('/nomnieks', methods=['POST', 'GET'])
def nomnieki():
    if request.method == "POST":
        id_nomnieks = request.form["id_nomnieks"]
        vards = request.form["vards"]
        uzvards = request.form["uzvards"]
        talrunis = request.form["talrunis"]
        a = [id_nomnieks,vards,uzvards,talrunis]
        db = sqlite3.connect('noma.db')
        sql = db.cursor()
        sql.execute("INSERT INTO nomnieks VALUES(?,?,?,?)",a)
        db.commit()
        db.close()
    return render_template('nomnieks.html')

@app.route('/instrumenti', methods=['POST', 'GET'])
def instrumenti():
    if request.method == "POST":
        id_instruments = request.form["id_instruments"]
        instruments = request.form["instruments"]
        data = request.form["data"]
        cena = request.form["cena"]
        b = [id_instruments,instruments,data,cena]
        db = sqlite3.connect('noma.db')
        sql = db.cursor()
        sql.execute("INSERT INTO instrumenti VALUES(?,?,?,?)",b)
        db.commit()
        db.close()
    return render_template('instrumenti.html')


@app.route('/noma', methods=['POST', 'GET'])
def noma():
  if request.method == "POST":
      id_noma = request.form["id_noma"]
      id_nomnieks = request.form["id_nomnieks"]
      id_instruments = request.form["id_instruments"]
      c = [id_noma,id_nomnieks,id_instruments]
      db = sqlite3.connect('noma.db')
      sql = db.cursor()
      sql.execute("INSERT INTO noma VALUES(?,?,?)",c)
      db.commit()
      db.close()
  return render_template("noma.html")

@app.route('/kopa', methods=['POST', 'GET'])
def kopa():
  db = sqlite3.connect('noma.db')
  sql = db.cursor()
  sql.execute("SELECT vards,uzvards,instruments,data FROM noma JOIN nomnieks ON nomnieks.id_nomnieks = noma.id_nomnieks JOIN instrumenti ON instrumenti.id_instruments = noma.id_instruments")
  records = sql.fetchall()
  print(records)
  return render_template("kopa.html", rows = records)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)


# records = sql.fetchall()
#   print(records)