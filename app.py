from flask import Flask, request, jsonify
from models.meal import Meal
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)


@app.route('/meal', methods=["POST"])
def create_meal():
    data = request.json
    id = data.get("id")
    nome = data.get("nome")
    descricao = data.get("descricao")
    data_hora = data.get("data_hora")
    dentro_da_dieta = data.get("dentro_da_dieta")
    user_id = data.get("user_id")
    

    if nome is None or dentro_da_dieta is None:
        return jsonify({"message": "Nome e dentro_da_dieta são obrigatórios"}),400

    if data_hora:
        from datetime import datetime
        data_hora = datetime.fromisoformat(data_hora)
    else:
        data_hora = datetime.utcnow()
    

    meal = Meal( nome=nome,
                descricao=descricao,
                data_hora=data_hora,
                dentro_da_dieta=dentro_da_dieta
                ,user_id=user_id)
                
    
    db.session.add(meal)
    db.session.commit()

    return jsonify({"message":"refeição criada com sucesso"})
        

@app.route('/meal/<int:id>', methods=['PUT'])
def update_meal(id):
    data = request.json
    meal = Meal.query.get(id)

    if not meal:
        return jsonify({"Message": "Refeição não encontrada"}),404      


    data = request.json
    if "nome" in data:
        meal.nome = data["nome"]
    if "descricao" in data:
        meal.descricao = data["descricao"]
    if "dentro_da_dieta" in data:
        if isinstance(data["dentro_da_dieta"], str):
            meal.dentro_da_dieta = data["dentro_da_dieta"].lower() == 'true'
        else:
            meal.dentro_da_dieta = bool(data["dentro_da_dieta"])
    if "data_hora" in data:
        from datetime import datetime
        meal.data_hora = datetime.fromisoformat(data["data_hora"])

    db.session.commit()
    return jsonify({"message":"refeição atualizada com sucesso"})


@app.route('/meal/<int:id>', methods=['DELETE'])
def delete_meal(id):
    meal = Meal.query.get(id)
    if not meal:
        return jsonify({"Message": "Refeição não encontrada"}),404     

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Usuario {id} deletado com sucesso"})


@app.route('/meals/<int:user_id>', methods=['GET'])
def list_meals(user_id):
    meals = Meal.query.filter_by(user_id=user_id).all()
    if not meals:
        return jsonify({"message": "Nenhuma refeição encontrada para este usuário"}), 404

    return jsonify([
        {
            "id": meal.id,
            "nome": meal.nome,
            "descricao": meal.descricao,
            "data_hora": meal.data_hora.isoformat(),
            "dentro_da_dieta": meal.dentro_da_dieta
        }
        for meal in meals
    ]), 200


@app.route('/meal/<int:id>', methods=['GET'], endpoint="get_meal")
def get_meal(id):
    meal = Meal.query.get(id)
    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404

    return jsonify({
        "id": meal.id,
        "nome": meal.nome,
        "descricao": meal.descricao,
        "data_hora": meal.data_hora.isoformat() if meal.data_hora else None,
        "dentro_da_dieta": meal.dentro_da_dieta,
        "user_id": meal.user_id
    })





if  __name__ == '__main__':
    app.run(debug=True)