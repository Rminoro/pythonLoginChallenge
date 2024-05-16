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
from flask_cors import CORS


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
        'email': email,  # Adiciona o e-mail ao registro do usuário
        'token_recuperacao': ''  
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

    users_ref = db.collection('usuarios')
    query = users_ref.where('cpf', '==', cpf).where('email', '==', email)
    snapshot = query.get()

    if len(snapshot) == 0:
        return jsonify({"success": False, "message": "CPF ou email não encontrados."}), 404

    token_recuperacao = 'abc123'

    for doc in snapshot:
        doc.reference.update({"token_recuperacao": token_recuperacao})
    
    print(f"Token de recuperação gerado para CPF {cpf} e email {email}: {token_recuperacao}")

    msg = Message('Recuperação de Senha', sender='seu_email@gmail.com', recipients=[email])
    msg.body = f'Olá,\n\nVocê solicitou a recuperação de senha. Use o seguinte token para redefinir sua senha: {token_recuperacao}\n\nAtenciosamente,\nSua Aplicação'

    try:
        mail.send(msg)
        print(f"E-mail de recuperação enviado para {email}.")
        return jsonify({"success": True, "message": "Token de recuperação enviado para o seu email."}), 200
    except Exception as e:
        print(f"Erro ao enviar e-mail de recuperação para {email}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    

@app.route('/redefinir_senha', methods=['POST'])
def redefinir_senha():
    # Receba os dados do formulário (cpf, email, token e nova senha)
    cpf = request.json.get('cpf')
    email = request.json.get('email')
    token = request.json.get('token')
    nova_senha = request.json.get('nova_senha')

    # Verifique se o CPF e o email fornecidos correspondem a um usuário
    users_ref = db.collection('usuarios')
    query = users_ref.where('cpf', '==', cpf).where('email', '==', email)
    snapshot = query.get()

    if len(snapshot) == 0:
        return jsonify({"success": False, "message": "CPF ou email não encontrados."}), 404

    # Verificar se o token recebido é válido para o usuário
    for doc in snapshot:
        user_data = doc.to_dict()
        if user_data.get('token_recuperacao') == token:
            # Atualizar a senha do usuário no Firestore
            doc.reference.update({"senha": nova_senha})
            print('Senha redefinida com sucesso para o usuário com CPF:', cpf)
            return jsonify({"success": True, "message": "Senha redefinida com sucesso."}), 200
        else:
            return jsonify({"success": False, "error": "Token de redefinição de senha inválido."}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
