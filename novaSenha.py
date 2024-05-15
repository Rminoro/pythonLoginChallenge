# Importe os módulos necessários
from flask import request,Flask, jsonify
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
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
        return jsonify({"success": True, "message": "Senha redefinida com sucesso."}), 200
    except Exception as e:
        # Em caso de erro, responda com uma mensagem de erro
        return jsonify({"success": False, "error": str(e)}), 400
