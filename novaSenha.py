# Importe os módulos necessários
from flask import request, Flask, jsonify
import firebase_admin
from firebase_admin import credentials, auth

# Inicialize o aplicativo Flask
app = Flask(__name__)

# Inicialize o SDK do Firebase com suas credenciais
cred = credentials.Certificate('./challengemobile-2a2e2-firebase-adminsdk-69efh-3bea316cc5.json')
firebase_admin.initialize_app(cred)

# Rota para redefinir a senha
@app.route('/redefinir_senha', methods=['POST'])
def redefinir_senha():
    # Receba os dados do formulário (token e nova senha)
    token = request.json.get('token')
    nova_senha = request.json.get('nova_senha')

    try:
        # Verifique se o token é válido
        decoded_token = auth.verify_password_reset_link(token)
        
        # Obtenha o ID do usuário a partir do token
        user_id = decoded_token['user_id']
        
        # Atualize a senha do usuário no Firebase Authentication
        auth.update_user(user_id, password=nova_senha)
        
        # Responda com uma mensagem de sucesso
        response_data = {"success": True, "message": "Senha redefinida com sucesso."}
        return jsonify(response_data), 200
    except Exception as e:
        # Em caso de erro, responda com uma mensagem de erro
        error_message = str(e)
        return jsonify({"success": False, "error": error_message}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
