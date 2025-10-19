from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import requests
import os
from datetime import timedelta, datetime
from functools import wraps
import msal
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Armazenamento temporario para os tokens ( bloqueio de cookies cross-domain Google )
temp_tokens = {}

def clean_expired_tokens():
    """Remove tokens expirados (mais de 5 minutos)"""
    now = datetime.now()
    expired = [token for token, data in temp_tokens.items() 
               if (now - data.get('created_at', now)).total_seconds() > 300]
    for token in expired:
        temp_tokens.pop(token, None)

# CORS
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",
    "http://localhost:8080",
    os.environ.get("FRONTEND_URL", "")
])

# OAuth
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
TENANT_ID = os.environ.get("AZURE_TENANT_ID", "common")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/auth/callback"
SCOPE = ["User.Read", "Contacts.Read"]

#MSAL
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)


def require_auth(f):
    #checar se ta logado
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica a authorization header primeiro
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            clean_expired_tokens()
            temp_data = temp_tokens.get(token)
            if temp_data:
                # Injeta o access_token temporariamente para o endpoint usar
                request.temp_access_token = temp_data.get('access_token')
                request.temp_refresh_token = temp_data.get('refresh_token')
                return f(*args, **kwargs)
        
        # Fallback para sessão normal
        if 'access_token' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return jsonify({
        "message": "Meus Contatos MS - API",
        "version": "1.0.0",
        "status": "running"
    })


@app.route('/auth/login')
def login():
    
    session["state"] = os.urandom(16).hex()
    
    redirect_uri = url_for('callback', _external=True, _scheme='https')
    
    auth_url = msal_app.get_authorization_request_url(
        SCOPE,
        state=session["state"],
        redirect_uri=redirect_uri
    )
    
    return redirect(auth_url)


@app.route('/auth/callback')
def callback():
    """Callback após autenticação"""
    if request.args.get('state') != session.get("state"):
        return jsonify({"error": "Invalid state parameter"}), 400
    
    if "error" in request.args:
        return jsonify({"error": request.args.get("error")}), 400
    
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "No code received"}), 400
    
    redirect_uri = url_for('callback', _external=True, _scheme='https')
    
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=redirect_uri
    )
    
    if "error" in result:
        return jsonify({"error": result.get("error_description")}), 400
    
    session['access_token'] = result['access_token']
    session['refresh_token'] = result.get('refresh_token')
    session['user_id'] = result.get('id_token_claims', {}).get('oid')
    session.permanent = True
    
    #  token tempoarrio e armazena emm memoria ( PARA NÃO OS USAR COOKIES! )
    temp_token = os.urandom(32).hex()
    clean_expired_tokens()
    temp_tokens[temp_token] = {
        'access_token': result['access_token'],
        'refresh_token': result.get('refresh_token'),
        'user_id': result.get('id_token_claims', {}).get('oid'),
        'created_at': datetime.now()
    }
    
    # --> frontend <---
    frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")
    return redirect(f"{frontend_url}/contacts?auth=success&token={temp_token}")


@app.route('/auth/exchange-token', methods=['POST'])
def exchange_token():
    """Troca token temporário por sessão permanente"""
    data = request.get_json()
    temp_token = data.get('token')
    
    if not temp_token:
        return jsonify({"error": "No token provided"}), 400
    
    clean_expired_tokens()
    token_data = temp_tokens.get(temp_token)
    
    if not token_data:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    # Copia dados do token para a sessão principal
    session['access_token'] = token_data['access_token']
    session['refresh_token'] = token_data['refresh_token']
    session['user_id'] = token_data['user_id']
    session.permanent = True
    
    return jsonify({"success": True})


@app.route('/auth/status')
def auth_status():
    """Verifica status de autenticação"""
    # Verifica se tem token no header Authorization
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        clean_expired_tokens()
        # Verifica se o token está válido em memória
        temp_data = temp_tokens.get(token)
        if temp_data:
            return jsonify({
                "authenticated": True,
                "user_id": temp_data.get('user_id'),
                "access_token": temp_data.get('access_token')
            })
    
    # Fallback -> back sessão normal
    return jsonify({
        "authenticated": 'access_token' in session,
        "user_id": session.get('user_id')
    })


@app.route('/auth/logout')
def logout():
    """Faz logout do usuário"""
    session.clear()
    return jsonify({"message": "Logged out successfully"})


@app.route('/api/contacts')
@require_auth
def get_contacts():
    """Busca contatos do usuário e agrupa por domínio"""
    access_token = getattr(request, 'temp_access_token', None) or session.get('access_token')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Start Contact Request to Microsoft Graph API
    graph_url = 'https://graph.microsoft.com/v1.0/me/contacts'
    
    try:
        response = requests.get(graph_url, headers=headers)
        
        if response.status_code == 401:
            
            if 'refresh_token' in session:
                result = msal_app.acquire_token_by_refresh_token(
                    session['refresh_token'],
                    scopes=SCOPE
                )
                if 'access_token' in result:
                    session['access_token'] = result['access_token']
                    headers['Authorization'] = f'Bearer {result["access_token"]}'
                    response = requests.get(graph_url, headers=headers)
                else:
                    session.clear()
                    return jsonify({"error": "Token expired"}), 401
            else:
                session.clear()
                return jsonify({"error": "Token expired"}), 401
        
        response.raise_for_status()
        contacts_data = response.json()
        
        # Agrupamento para contatos de dominio
        grouped_contacts = {}
        
        for contact in contacts_data.get('value', []):
            email_addresses = contact.get('emailAddresses', [])
            
            for email_obj in email_addresses:
                email = email_obj.get('address', '')
                if email and '@' in email:
                    domain = email.split('@')[1]
                    
                    if domain not in grouped_contacts:
                        grouped_contacts[domain] = []
                    
                    grouped_contacts[domain].append({
                        'id': contact.get('id'),
                        'displayName': contact.get('displayName', 'Sem nome'),
                        'email': email,
                        'givenName': contact.get('givenName', ''),
                        'surname': contact.get('surname', ''),
                        'jobTitle': contact.get('jobTitle', ''),
                        'companyName': contact.get('companyName', ''),
                        'mobilePhone': contact.get('mobilePhone', ''),
                        'businessPhones': contact.get('businessPhones', [])
                    })
        
        # Ordena domínios e contatos
        result = []
        for domain in sorted(grouped_contacts.keys()):
            result.append({
                'domain': domain,
                'count': len(grouped_contacts[domain]),
                'contacts': sorted(grouped_contacts[domain], key=lambda x: x['displayName'])
            })
        
        return jsonify({
            'success': True,
            'total_domains': len(result),
            'total_contacts': sum(d['count'] for d in result),
            'data': result
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/user/profile')
@require_auth
def get_user_profile():
    """Busca informações do usuário logado"""
    access_token = getattr(request, 'temp_access_token', None) or session.get('access_token')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        response.raise_for_status()
        user_data = response.json()
        
        return jsonify({
            'success': True,
            'user': {
                'id': user_data.get('id'),
                'displayName': user_data.get('displayName'),
                'mail': user_data.get('mail'),
                'userPrincipalName': user_data.get('userPrincipalName'),
                'jobTitle': user_data.get('jobTitle'),
                'officeLocation': user_data.get('officeLocation')
            }
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')

