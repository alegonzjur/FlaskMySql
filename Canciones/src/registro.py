# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:44:32 2023

@author: agonjur
"""

from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

@app.route('/')
def registro():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario.
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('create.html', data=insertObject)

@app.route('/registro', methods=['POST'])
def addUser():
    user = request.form['user']
    password = request.form['password']
    conf_pass = request.form['conf_pass']
    if user and password and conf_pass == password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (user,password) VALUES (%s, %s)"
        data = (user,password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('registro'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)