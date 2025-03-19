from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="reservaciones"
    )

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas")
    citas = cursor.fetchall()
    conn.close()
    return render_template('index.html', citas=citas)

@app.route('/add', methods=['POST'])
def add():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO citas (cliente, fecha, hora, estado) VALUES (%s, %s, %s, %s)",
                   (request.form['cliente'], request.form['fecha'], request.form['hora'], "pendiente"))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE citas SET cliente = %s, fecha = %s, hora = %s, estado = %s WHERE id = %s",
                   (request.form['cliente'], request.form['fecha'], request.form['hora'], request.form['estado'], id))
    conn.commit()
    conn.close()
    return redirect('/')
