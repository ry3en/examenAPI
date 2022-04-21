from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    nivel = db.Column(db.String(255))
    t_min = db.Column(db.Integer)
    kalo = db.Column(db.Integer)
    cal = db.Column(db.Integer)
    ingrediente_p = db.Column(db.String(255))
    ingredientes_s = db.Column(db.String(255))
    d_receta = db.Column(db.String(255))

    def __init__(self, nombre, nivel, t_min, kalo, cal, ingrediente_p, ingredientes_s, d_receta):
        self.nombre = nombre
        self.nivel = nivel
        self.t_min = t_min
        self.kalo = kalo
        self.cal = cal
        self.ingrediente_p = ingrediente_p
        self.ingredientes_s = ingredientes_s
        self.d_receta = d_receta

# Crea la base de datos se comenta despues
db.create_all()


class RecipeSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "nivel", "t_min", "kalo", "cal", "ingrediente_p", "ingrediente_s", "d_receta")


recipeSchema = RecipeSchema()

recipeSchema = RecipeSchema(many=True)

recipes = [{}]

recetas = Recipe.query.all()
print(recetas)


@app.route("/")
def hello_world():
    return "Hola Mundo"


@app.route("/api/recetas/", methods=["GET"])
def get_recipes():
    return jsonify({"recipes": recetas})


@app.route("/api/recetas/" + "<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify({"recipe": recipe})


@app.route("/api/recetas/", methods=["POST"])
def create_recipe():
    if not request.json:
        abort(404)
    new_recipe = Recipe(nombre=request.json["nombre"], nivel=request.json["nivel"], t_min=request.json["t_min"],
                        kalo=request.json["kalo"],  cal=request.json["cal"], ingrediente_p=request.json["ingrediente_p"],
                        ingredientes_s=request.json["ingredientes_s"], d_receta=request.json["d_receta"])
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"recipe": new_recipe}), 201


@app.route("/api/recetas/" + "<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    if not request.json:
        abort(400)

    recipe = Recipe.query.get_or_404(recipe_id)

    recipe.nombre = request.json["nombre"]
    recipe.nivel = request.json["nivel"]
    recipe.t_min = request.json["t_min"]
    recipe.kalo = request.json["kalo"]
    recipe.cal = request.json["cal"]
    recipe.ingrediente_p = request.json["ingrediente_p"]
    recipe.ingredientes_s = request.json["ingredientes_s"]
    recipe.d_receta = request.json["d_receta"]
    db.session.commit()

    return jsonify({"recipe": Recipe.as_dict(recipe)}), 201


@app.route("/api/recetas/" + "<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True)
