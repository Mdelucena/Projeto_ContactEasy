# ContatoFácil

Sistema para gerenciar contatos Microsoft organizados por domínio de email.

## Stack

**Frontend:** Vue.js 3, Vue Router, Pinia, Vue I18n  
**Backend:** Python 3.11, Flask, Microsoft Graph API  
**Deploy:** Firebase Hosting + Google Cloud Run

## Como executar localmente

### Backend

Primeiro, configure o App Registration no Azure Portal:
- Vá em Azure Active Directory > App registrations > New registration
- Adicione a redirect URI: `http://localhost:5000/auth/callback`
- Crie um Client Secret em Certificates & secrets
- Adicione as permissões: `User.Read` e `Contacts.Read`

Depois, rode o backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crie um arquivo `.env` com suas credenciais:

```env
AZURE_CLIENT_ID=seu-client-id
AZURE_CLIENT_SECRET=seu-client-secret
AZURE_TENANT_ID=common
SECRET_KEY=uma-chave-aleatoria-qualquer
FLASK_ENV=development
PORT=5000
FRONTEND_URL=http://localhost:5173
```

Rode:
```bash
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse: `http://localhost:5173`

## Funcionalidades implementadas

- ✅ Autenticação OAuth2 com Microsoft
- ✅ Listagem de contatos via Graph API
- ✅ Agrupamento por domínio de email
- ✅ Proteção de rotas (Vue Router)
- ✅ Multi-idioma (PT/EN)
- ✅ Busca e filtragem
- ✅ Interface responsiva

## Deploy em produção

**Backend:** Google Cloud Run  
**Frontend:** Firebase Hosting

URLs:
- Frontend: https://contatofacil-a27f4.web.app
- Backend: https://meus-contatos-backend-570939512497.us-central1.run.app

## Observações

O sistema usa tokens temporários em memória no backend para evitar problemas com cookies cross-domain. Os tokens ficam armazenados no localStorage do frontend e são enviados via header Authorization.

---
