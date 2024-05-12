from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

# Inicializa o Firebase
cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
firebase_app = initialize_app(cred)
db = firestore.client()

# Cria o blueprint para o registro
register_blueprint = Blueprint('register', __name__)

# Variável global para manter o contador do ID
id_counter = 1

# Endpoint para registro (cadastro) de usuário
@register_blueprint.route('/register', methods=['POST'])
def register():
    global id_counter  # Utiliza a variável global id_counter

    data = request.get_json()
    cpf = data.get('cpf')
    senha = data.get('senha')

    # Verifica se o CPF já está cadastrado
    users_ref = db.collection('usuarios')
    query = users_ref.where('cpf', '==', cpf)
    snapshot = query.get()

    if len(snapshot) > 0:
        return jsonify({"success": False, "message": "CPF já cadastrado."}), 400

    # Gera o novo ID automaticamente
    id = id_counter
    id_counter += 1

    # Cria um novo usuário no Firestore
    new_user_ref = users_ref.document()
    new_user_ref.set({
        'id': id,
        'cpf': cpf,
        'senha': senha
    })

    return jsonify({"success": True, "message": "Usuário registrado com sucesso.", "id": id}), 200
