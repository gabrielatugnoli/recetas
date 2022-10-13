from email import message
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app

from flask_app.models.users import User
from flask_app.models.recipes import Recipe


#Importación de BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #validamos la info que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')

    #guardamos registro
    pwd = bcrypt.generate_password_hash(request.form['password']) #encriptando la password del usuario y la guardamos en pwd

    #creamos un diccionario con todos los datos del request.form
    #creamos un neuvo diccionario porque request.form es un objeto (diccionario) inmutable y no se puede cambiar, daria error si quisieramos reemplazar la contrase;a original por la encriptada
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #recibimos el id del nuevo usuario

    session['user_id'] = id #guardamos en sesion el id del usuario

    return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session: #aqui restringo la posibilidad de entrar sin haber iniciado sesion
        return redirect('/')

    formulario = { "id": session['user_id']}

    user = User.get_by_id(formulario)

    recipes = Recipe.get_all()
    
    return render_template('home.html', user=user, recipes=recipes)

@app.route('/login', methods=['POST'])
def login():
    #verificamos que el email exista en la base de datos
    user = User.get_by_email(request.form) #recibimos una instancia de usuario o false

    if not user: #si user = false
        flash('Email no encontrado', 'login')
        return redirect('/')
        #return jsonify(message="Email no encontrado")

    #user es una instancia
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')
        #return jsonify(message="Password incorrecto")


    session['user_id'] = user.id
    return redirect ('/home')
    #return jsonify(message="correcto")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')