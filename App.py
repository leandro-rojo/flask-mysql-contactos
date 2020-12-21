from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lambda'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)

# Configuracion secret_key para jinja
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    datos=cur.fetchall()
    return render_template('index.html', contactos=datos)

@app.route('/add', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (nombre, telefono, correo) VALUES (%s, %s, %s)', (nombre, telefono, correo))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')
        return redirect(url_for('Index')) 

@app.route('/editar/<id>')
def editar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id=%s', [id])
    dato=cur.fetchall()
    return render_template('editar.html',contacto=dato[0])

@app.route('/update/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contactos SET nombre=%s, telefono=%s, correo=%s WHERE id=%s', (nombre, telefono, correo, id))
        mysql.connection.commit()
        flash('Contacto modificado satisfactoriamente')
        return redirect(url_for('Index')) 

@app.route('/eliminar/<id>')
def eliminar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = %s',[format(id)])
    mysql.connection.commit()
    flash('Contacto Eliminado satisfactoriamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 8000, debug = True)
