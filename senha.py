import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'sua_senha'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Inicializa o Firebase Admin SDK
cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Rota para solicitar recuperação de senha
@app.route('/solicitar_recuperacao_senha', methods=['POST'])
def solicitar_recuperacao_senha():
    data = request.get_json()
    email = data.get('email')

    # Consulta o Firestore para verificar se o e-mail fornecido existe
    users_ref = db.collection('usuarios')
    query = users_ref.where('email', '==', email)
    snapshot = query.get()

    if len(snapshot) == 0:
        return jsonify({"success": False, "message": "E-mail não encontrado."}), 404
    
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

if __name__ == '__main__':
    app.run(debug=True)
