import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="comentarios",
  password="comentarios",
  database="comentarios"
)


def query(sql):
    cur = db.cursor(dictionary=True)
    cur.execute(sql)
    if sql.upper().startswith('SELECT'):
        return cur.fetchall()
    db.commit()
    if sql.upper().startswith('INSERT'):
        return cur.lastrowid


