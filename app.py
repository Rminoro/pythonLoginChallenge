# import firebase_admin
# from firebase_admin import credentials, firestore
# from flask import Flask, request, jsonify

# # Inicializa o aplicativo Flask
# app = Flask(__name__)

# # Carrega as credenciais do Firebase
# cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
# firebase_admin.initialize_app(cred)

# # Inicializa o Firestore
# db = firestore.client()

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     id = data.get('id')
#     cpf = data.get('cpf')
#     senha = data.get('senha')

#     # Consulta o Firestore para verificar se o usuário existe e a senha está correta
#     users_ref = db.collection('usuarios')
#     query = users_ref.where('cpf', '==', cpf).where('senha', '==', senha)
#     snapshot = query.get()

#     if len(snapshot) == 1:
#         user_data = snapshot[0].to_dict()
#         return jsonify({"success": True, "user": user_data}), 200
#     else:
#         return jsonify({"success": False, "message": "CPF ou senha inválidos."}), 401

# if __name__ == '__main__':
#     app.run(debug=True)

# ##########################################

# import firebase_admin
# from firebase_admin import credentials, firestore
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     cpf = data.get('cpf')
#     senha = data.get('senha')

#     users_ref = db.collection('usuarios')
#     query = users_ref.where('cpf', '==', cpf).where('senha', '==', senha)
#     snapshot = query.get()

#     if len(snapshot) == 1:
#         user_data = snapshot[0].to_dict()
#         return jsonify({"success": True, "user": user_data}), 200
#     else:
#         return jsonify({"success": False, "message": "CPF ou senha inválidos."}), 401

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
# ################################################
# import firebase_admin
# import random
# from firebase_admin import credentials, firestore
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     cpf = data.get('cpf')
#     senha = data.get('senha')

#     users_ref = db.collection('usuarios')
#     query = users_ref.where('cpf', '==', cpf).where('senha', '==', senha)
#     snapshot = query.get()

#     if len(snapshot) == 1:
#         user_data = snapshot[0].to_dict()
#         return jsonify({"success": True, "user": user_data}), 200
#     else:
#         return jsonify({"success": False, "message": "CPF ou senha inválidos."}), 401
# #############################################
# ##########################################
# #################################
# # @app.route('/register', methods=['POST'])
# # def register():
# #     data = request.get_json()
# #     cpf = data.get('cpf')
# #     senha = data.get('senha')

# #     users_ref = db.collection('usuarios')
# #     query = users_ref.where('cpf', '==', cpf)
# #     snapshot = query.get()

# #     if len(snapshot) > 0:
# #         return jsonify({"success": False, "message": "CPF já cadastrado."}), 400

# #     new_user_ref = users_ref.document()
# #     new_user_ref.set({
# #         'cpf': cpf,
# #         'senha': senha
# #     })

# #     return jsonify({"success": True, "message": "Usuário registrado com sucesso."}), 200

# # if __name__ == '__main__':
# #     app.run(debug=True, host='0.0.0.0')
# # Endpoint para registro (cadastro) de usuário
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     cpf = data.get('cpf')
#     senha = data.get('senha')

#     # Gera o novo ID automaticamente
#     id = random.randint(100000, 999999)  # Exemplo de geração automática de ID

#     # Cria um novo usuário no Firestore
#     new_user_ref = db.collection('usuarios').document(str(id))
#     new_user_ref.set({
#         'id': id,
#         'cpf': cpf,
#         'senha': senha
#     })

#     return jsonify({"success": True, "message": "Usuário registrado com sucesso.", "id": id}), 200

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
import firebase_admin
import random
from firebase_admin import credentials, firestore, auth
from flask import Flask, request, jsonify
from flask_mail import Mail, Message


app = Flask(__name__)

cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cpf = data.get('cpf')
    senha = data.get('senha')

    users_ref = db.collection('usuarios')
    query = users_ref.where('cpf', '==', cpf).where('senha', '==', senha)
    snapshot = query.get()

    if len(snapshot) == 1:
        user_data = snapshot[0].to_dict()
        return jsonify({"success": True, "user": user_data}), 200
    else:
        return jsonify({"success": False, "message": "CPF ou senha inválidos."}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    cpf = data.get('cpf')
    senha = data.get('senha')
    email = data.get('email')  # Adicionado o campo de e-mail

    # Verifica se o CPF já está cadastrado
    users_ref = db.collection('usuarios')
    query = users_ref.where('cpf', '==', cpf)
    snapshot = query.get()

    if len(snapshot) > 0:
        return jsonify({"success": False, "message": "CPF já cadastrado."}), 400

    # Gera o novo ID automaticamente
    id = random.randint(100000, 999999)  # Exemplo de geração automática de ID

    # Cria um novo usuário no Firestore
    new_user_ref = db.collection('usuarios').document(str(id))
    new_user_ref.set({
        'id': id,
        'cpf': cpf,
        'senha': senha,
        'email': email  # Adiciona o e-mail ao registro do usuário
    })

    return jsonify({"success": True, "message": "Usuário registrado com sucesso.", "id": id}), 200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        # Acesse a coleção de usuários
        users_ref = db.collection('usuarios')

        # Obtenha todos os documentos da coleção
        docs = users_ref.stream()

        # Inicialize uma lista para armazenar os usuários
        usuarios = []

        # Itere sobre os documentos e adicione-os à lista de usuários
        for doc in docs:
            usuario = doc.to_dict()
            usuario['id'] = doc.id
            usuarios.append(usuario)

        # Retorne a lista de usuários como uma resposta JSON
        return jsonify(usuarios), 200
    except Exception as e:
        # Em caso de erro, retorne uma mensagem de erro com status 500
        return jsonify({"error": str(e)}), 500
    
##Recuperação de senha
# Configurações do email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ntjntjntjntj1@gmail.com'
app.config['MAIL_PASSWORD'] = 'vpti ctyk nbha lazw'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Rota para recuperar a senha
@app.route('/recuperar_senha', methods=['POST'])
def recuperar_senha():
    data = request.get_json()
    cpf = data.get('cpf')
    email = data.get('email')

    # Verificar se o CPF e o email fornecidos correspondem a um usuário
    users_ref = db.collection('usuarios')
    query = users_ref.where('cpf', '==', cpf).where('email', '==', email)
    snapshot = query.get()

    if len(snapshot) == 0:
        return jsonify({"success": False, "message": "CPF ou email não encontrados."}), 404

    # Simulação de um token de recuperação gerado
    token_recuperacao = 'abc123'

    # Enviar email com o token de recuperação
    msg = Message('Recuperação de Senha', sender='seu_email@gmail.com', recipients=[email])
    msg.body = f'Olá,\n\nVocê solicitou a recuperação de senha. Use o seguinte token para redefinir sua senha: {token_recuperacao}\n\nAtenciosamente,\nSua Aplicação'

    try:
        mail.send(msg)
        return jsonify({"success": True, "message": "Token de recuperação enviado para o seu email."}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
# RETORNA TOKEN E REDEFINE SENHA  

@app.route('/redefinir_senha', methods=['POST'])
def redefinir_senha():
    # Recebe os dados do formulário (email e nova senha)
    email = request.json.get('email')
    nova_senha = request.json.get('nova_senha')

    try:
        # Busca o usuário pelo email
        user_id = get_user_id_by_email(email)
        
        if user_id:
            # Define a nova senha para o usuário
            auth.update_user(user_id, password=nova_senha)
            
            # Responde com uma mensagem de sucesso
            return jsonify({"success": True, "message": "Senha redefinida com sucesso."}), 200
        else:
            # Se não encontrar um usuário com o email fornecido, responde com um erro
            return jsonify({"success": False, "error": "Usuário não encontrado."}), 404
    except Exception as e:
        # Em caso de erro, responde com uma mensagem de erro
        return jsonify({"success": False, "error": str(e)}), 400

def get_user_id_by_email(email):
    # Consulta para buscar o ID do usuário pelo email na subcoleção 'usuarios'
    query = db.collection('usuarios').document('usuarios').collection('usuarios').where('email', '==', email)
    snapshot = query.get()

    user_ids = []
    for doc in snapshot:
        user_id = doc.id
        user_ids.append(user_id)

    if user_ids:
        return user_ids[0]  # Retorna o primeiro ID encontrado
    else:
        return None
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
