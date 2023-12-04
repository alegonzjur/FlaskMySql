# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:12:08 2023

@author: agonjur
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

@app.route('/login', methods=['GET','POST'])
def login():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario.
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('log.html', data=insertObject)

@app.route('/dashboard', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'user' in request.form and 'password' in request.form:
        user = str(request.form['user'])
        password = str(request.form['password'])
        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM users WHERE user = %s", [user])
        account = cursor.fetchone
        if account:
            if check_password_hash(account['password'],password):
                msg = 'Ha iniciado sesion correctamente.'
                return render_template

@app.route('/registro', methods=['GET','POST'])
def registro():
    msg = ''
    if request.method == 'POST':
        user = request.method['user']
        password = request.method['password']
        conf_pass = request.method['conf_pass']
        
        #Comprobar si existe la cuenta.
        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM login WHERE user = %s", (user,))
        account = cursor.fetchone()
        cursor.close()
        
        if account:
            msg = 'Ese usuario ya existe.'
        elif password != conf_pass:
            msg = 'Las contraseñas no coinciden.'
        elif not user or not password or not conf_pass:
            msg = 'Completa todos los campos.'
        else:
            cursor = db.database.cursor()
            cursor.execute('INSERT INTO login (user,password) VALUES (%s, %s)')
            cursor.close()
            msg = 'Cuenta creada correctamente.'
        return render_template('index.html', msjAlert=msg, typeAlert=1)
    return render_template()
    
if __name__ == '__main__':
    app.run(debug=True, port=4000)