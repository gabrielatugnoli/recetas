from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.image = data['image']

        #LEFT JOIN
        self.first_name = data['first_name']

    @staticmethod
    def valida_receta(formulario):
        es_valido = True

        if len(formulario['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False

        if len(formulario['instructions']) < 3:
            flash('Las instrucciones deben tener al menos 3 caracteres', 'receta')
            es_valido = False

        if len(formulario['description']) < 3:
            flash('La descripción deben tener al menos 3 caracteres', 'receta')
            es_valido = False

        if len(formulario['date_made']) == '':
            flash('Ingrese fecha', 'receta')
            es_valido = False
        
        return es_valido
        

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO recipes (name,description,instructions,date_made,under_30,user_id,image) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s, %(user_id)s,%(image)s);"
        result = connectToMySQL('recetas').query_db(query,formulario)

        return result #regresa el id del nuevo registro que se realizó

    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*,users.first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('recetas').query_db(query)
        recipes = []

        for recipe in results:
            #recipe = diccionario con todas las columnas
            recipes.append(cls(recipe))

        return recipes

    @classmethod
    def get_by_id(cls,formulario):
        query = "SELECT recipes.*,users.first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL('recetas').query_db(query,formulario)

        recipe = cls(result[0])

        return recipe

    @classmethod
    def update(cls,formulario):
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s,instructions=%(instructions)s,date_made=%(date_made)s,under_30=%(under_30)s,image=%(image)s WHERE id=%(id)s" #el nombre de ese ultimo id debe ser igual al que recibimos en el formulario edit_recipe.html
        result = connectToMySQL('recetas').query_db(query,formulario)
        return result


    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query,formulario)
        return result