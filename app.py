import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Carrega as credenciais do Firebase
cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
firebase_admin.initialize_app(cred)

# Inicializa o Firestore
db = firestore.client()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    id = data.get('id')
    cpf = data.get('cpf')
    senha = data.get('senha')

    # Consulta o Firestore para verificar se o usuário existe e a senha está correta
    users_ref = db.collection('usuarios')
    query = users_ref.where('cpf', '==', cpf).where('senha', '==', senha)
    snapshot = query.get()

    if len(snapshot) == 1:
        user_data = snapshot[0].to_dict()
        return jsonify({"success": True, "user": user_data}), 200
    else:
        return jsonify({"success": False, "message": "CPF ou senha inválidos."}), 401

if __name__ == '__main__':
    app.run(debug=True)
