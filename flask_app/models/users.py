from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def valida_usuario(formulario):
        #formulario = DICCIONARIO con todos los names y valores que ingresa el user
        es_valido = True

        #validamos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('Nombre debe tener al menos 3 caracteres', 'registro')
            es_valido = False

        if len(formulario['last_name']) < 3:
            flash('Nombre debe tener al menos 3 caracteres', 'registro')
            es_valido = False

        if len(formulario['password']) < 6:
            flash('Password debe tener al menos 6 caracteres', 'registro')
            es_valido = False

        #verificamos que las contrase;as coincidan
        if formulario['password'] != formulario['confirm_password']:
            flash('Passwords no coinciden', 'registro')
            es_valido = False
        
        #verificamos que tengan el formato correcto
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail inválido', 'registro')
            es_valido = False

        #verificamos que la contrase;a tenga el formato correcto
        if not PASSWORD_REGEX.match(formulario['password']):
            flash('Password debe contener al menos una mayúscula y un número', 'registro')
            es_valido = False

        #consultamos si existe el mail
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recetas').query_db(query,formulario)
        if len(results) >= 1:
            flash("Ya existe ese correo registrado")
            es_valido = False

        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        result = connectToMySQL('recetas').query_db(query,formulario)

        return result #regresa el id del nuevo registro que se realizó

    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recetas').query_db(query, formulario)

        if len(result) < 1: #significa que mi lista está vacía
            return False
        else:
            #me regresauna lista con un registro correspondiente al usuario de ese mail
            user = cls(result[0])
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        user = cls(result[0])

        return user