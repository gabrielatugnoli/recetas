from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.recipes import Recipe
from flask_app.models.users import User

#Importaciones para subir imagenes
from werkzeug.utils import secure_filename
import os


@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session: #aqui restringo la posibilidad de entrar sin haber iniciado sesion
        return redirect('/')

    formulario = { "id": session['user_id']}

    user = User.get_by_id(formulario)

    return render_template('new_recipe.html',user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session: #aqui restringo la posibilidad de entrar sin haber iniciado sesion
        return redirect('/')

    #validacion receta 
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    #validacion que haya subido algo
    if 'image' not in request.files:
        flash('No seleccionó ninguna imagen', 'receta')
        return redirect('/new/recipe')

    image = request.files['image'] #la variable donde guardo la imagen

    #Validamos que no esté vacío
    if image.filename == '':
        flash('Nombre de imagen vacío', 'receta')
        return redirect('/new/recipe')

    #generando de manera segura el nombre de la imagen
    nombre_imagen = secure_filename(image.filename)

    #guardamos la imagen
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))

    #diccionario con todos los datos del formulario
    formulario = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": int(request.form['under_30']),
        "user_id": request.form['user_id'],
        "image": nombre_imagen
    }

    #guardamos la receta
    Recipe.save(formulario)

    return redirect('/home')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #la instancia de la receta que se debe desplegar en editar - en base al ID que recibimos en URL
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session: #aqui restringo la posibilidad de entrar sin haber iniciado sesion
        return redirect('/')

    #validacion receta 
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id'])

    #guardamos la receta
    Recipe.update(request.form)

    return redirect('/home')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session: #aqui restringo la posibilidad de entrar sin haber iniciado sesion
        return redirect('/')
    
    formulario = {"id": id}
    Recipe.delete(formulario)

    return redirect('/home')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    if 'user_id' not in session: #aqui restringo la posibilidad de entrar sin haber iniciado sesion
        return redirect('/')

    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)

    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('show_recipe.html', user=user, recipe=recipe)
