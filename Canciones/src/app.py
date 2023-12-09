# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:12:08 2023

@author: agonjur
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import database as db
from database import * #Importamos la función de la base de datos.

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#La primera pantalla debe ser un login.
@app.route('/', methods=['GET', 'POST'])
def login():
    conexionMYSQL = conexionBD()
    if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
        user = request.form['user']
        password = request.form['password']
        #Comprobamos que la cuenta existe.
        cursor = conexionMYSQL.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE user = %s AND password = %s', (user,password))
        cuenta = cursor.fetchone()
        if cuenta:
            return redirect(url_for('home'))
    return render_template('log.html', msjAlert = 'Debe iniciar sesión.', typeAlert=0)
        
#Registro de usuario.
@app.route('/registro', methods=['GET','POST'])
def registro():
    msg = ''
    conexionMYSQL = conexionBD()
    if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
        user = request.form['user']
        password = str(request.form['password'])
        rep_pass = str(request.form['rep_pass'])

        #Comprobamos que no existe cuenta con ese usuario.
        cursor = conexionMYSQL.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE user = %s', [user])
        cuenta = cursor.fetchone()
        cursor.close()

        if cuenta:
            msg = 'Ya existe una cuenta asociada a ese usuario.'
        elif password != rep_pass:
            msg = 'Las contraseñas no coinciden.'
        elif not user or not password or not rep_pass:
            msg = 'Debes completar todos los campos.'
        else:
            #La cuenta no existe y los datos son validos.
            conexionMYSQL = conexionBD()
            cursor = conexionMYSQL.cursor(dictionary=True)
            cursor.execute('INSERT INTO users (user,password) VALUES (%s, %s)', (user,password))
            conexionMYSQL.commit()
            cursor.close()
            msg = 'Cuenta creada correctamente!'

        return redirect(url_for('login'))
    return render_template('create.html', msjAlert = msg, typeAlert=0)

#CRUD.
@app.route('/home')
def home():
    conexionMYSQL = conexionBD()
    cursor = conexionMYSQL.cursor()
    cursor.execute("SELECT * FROM canciones")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route('/song', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    genero = request.form['genero']
    cancion = request.form['cancion']
    album = request.form['album']
    if nombre and genero and cancion and album:
        conexionMYSQL = conexionBD()
        cursor = conexionMYSQL.cursor()
        sql = "INSERT INTO canciones (nombre, genero, cancion, album) VALUES (%s, %s, %s, %s)"
        data = (nombre, genero, cancion, album)
        cursor.execute(sql, data)
        conexionMYSQL.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    conexionMYSQL = conexionBD()
    cursor = conexionMYSQL.cursor()
    sql = "DELETE FROM canciones WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    conexionMYSQL.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    genero = request.form['genero']
    cancion = request.form['cancion']
    album = request.form['album']

    if nombre and genero and cancion and album:
        conexionMYSQL = conexionBD()
        cursor = conexionMYSQL.cursor()
        sql = "UPDATE canciones SET nombre = %s, genero = %s, cancion = %s, album = %s WHERE id = %s"
        data = (nombre, genero, cancion, album, id)
        cursor.execute(sql, data)
        conexionMYSQL.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)





