# Clube do Gole

Plataforma de e-commerce de assinatura de bebidas premium — catálogo de produtos com planos de recorrência (mensal, semestral, anual), carrinho, checkout, assinaturas e painel administrativo completo.

---

## Stack

### Backend
- **Python 3.10** + **FastAPI**
- **SQLAlchemy 2.0** (async) + SQLite (dev) / PostgreSQL (prod)
- **Pydantic v2** para validação de schemas
- Autenticação **JWT** (PyJWT + bcrypt) com controle de sessões
- Alembic para migrations

### Frontend
- **Vue.js 3** (Composition API) + **Vite**
- **Pinia** para gerenciamento de estado
- **Vue Router** com guards de autenticação/admin
- **Axios** com interceptors de token
- Identidade visual: Cormorant Garamond + DM Sans

### CMS
- **Strapi** (headless CMS) — gerencia conteúdo editorial do site: blog, FAQ, banners da home, depoimentos, entregas anteriores e páginas institucionais (Sobre, Contato, Envio & Devoluções)

---

## Arquitetura

```
Clube_do_gole
├── backend
│   ├── app.py               # entrada FastAPI
│   ├── routes/              # endpoints (auth, produtos, carrinho, admin...)
│   ├── services/            # regras de negócio
│   ├── repositories/        # acesso a dados (SQLAlchemy)
│   ├── schemas/             # modelos Pydantic
│   ├── database/            # engine, models, seed
│   └── utils/               # JWT, email, helpers
└── frontend
    └── src
        ├── views/           # páginas (Home, Produto, Carrinho, Checkout...)
        │   └── admin/       # painel administrativo (ERP)
        ├── components/      # componentes reutilizáveis
        ├── stores/          # Pinia stores
        ├── services/        # camada de API (Axios)
        └── router/          # rotas + guards
```

---

## Funcionalidades

### Loja
- Catálogo de produtos com planos de assinatura e preços por recorrência
- Carrinho com seleção de itens, quantidade e exclusão
- Checkout com endereços (CRUD + busca por CEP), cupons de desconto e formas de pagamento
- Cadastro/login de clientes (JWT) e recuperação de senha
- Histórico de pedidos e assinaturas do cliente

### Painel Administrativo (ERP)
- Dashboard de vendas: faturamento, ticket médio, produtos mais vendidos
- Gestão de produtos e planos de assinatura (preço base, desconto por recorrência)
- Gestão de cupons (usos, validade, status)
- Controle de estoque por movimentações (entrada, saída, ajuste)
- Acompanhamento de assinaturas (ativar, pausar, cancelar)
- Histórico de pagamentos

---

## Modelo de negócio

Clube de assinatura com planos de recorrência:

| Plano | Ciclo | Desconto |
|---|---|---|
| Mensal | 30 dias | — |
| Semestral | 180 dias | configurável |
| Anual | 365 dias | configurável |

Cada produto possui planos independentes com preço e desconto próprios, calculados pelo backend.

---

## Como executar

### Pré-requisitos
- Python 3.10+
- Node.js 18+

### 1. Clonar o repositório
```bash
git clone https://github.com/Guilherme-FDS/Clube_do_gole.git
cd Clube_do_gole
```

### 2. Backend
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r backend/requirements.txt
cd backend
python -m uvicorn app:app --reload --port 8000
```

API disponível em `http://localhost:8000` — docs interativas em `http://localhost:8000/docs`.

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

Aplicação disponível em `http://localhost:5173`.

---

## Variáveis de ambiente

Backend (`backend/.env`):
```
DATABASE_URL=sqlite+aiosqlite:///./database/clube_do_gole.db
SECRET_KEY=<sua-chave>
MP_ACCESS_TOKEN=<seu-access-token-mercado-pago>
MP_PUBLIC_KEY=<sua-public-key-mercado-pago>
```

Frontend (`frontend/.env.local`):
```
VITE_API_URL=http://localhost:8000/api
VITE_STRAPI_URL=http://localhost:1337
```

---

## Testando pagamentos

Para testar o checkout com o Mercado Pago em modo sandbox, configure as credenciais de TESTE (prefixo `TEST-`) nas variáveis de ambiente `MP_ACCESS_TOKEN` e `MP_PUBLIC_KEY` (veja a seção de variáveis de ambiente). Com credenciais de teste, o Mercado Pago aceita apenas os dados fictícios abaixo — nenhum cartão, PIX ou boleto real é cobrado.

### Conta de teste (comprador)

Na hora de pagar no checkout do Mercado Pago (tela do próprio MP, fora do nosso site), use a conta de teste "comprador" abaixo para logar quando solicitado:

| Papel | Usuário | Senha |
|---|---|---|
| Comprador | `TESTUSER6108724104764143400` | `Zw3MoG9dw1` |

(Contas de teste do Mercado Pago são fictícias — não usam dados reais e não movimentam dinheiro real.)

### Cartões de crédito de teste

| Bandeira | Número | CVV | Validade | Resultado |
|---|---|---|---|---|
| Mastercard | 5031 4332 1540 6351 | 123 | 11/30 | Aprovado |
| Visa | 4235 6477 2802 5682 | 123 | 11/30 | Aprovado |
| Visa (recusado) | 4013 5406 8274 6260 | 123 | 11/30 | Recusado (fundos insuficientes) |

Nome do titular: `APRO` (aprova automaticamente) ou `OTHE` (recusa) — convenção oficial de sandbox do Mercado Pago.
CPF de teste: qualquer CPF válido gerado (ex: gerador online), ou `123.456.789-09`.

### PIX de teste

No sandbox, o QR code gerado é fictício. O próprio painel do Mercado Pago (conta de teste "vendedor", em [mercadopago.com.br](https://www.mercadopago.com.br)) tem uma opção para simular a confirmação do pagamento PIX manualmente.

### Boleto de teste

O sandbox gera um boleto fictício. O painel de testes do Mercado Pago também permite simular o pagamento do boleto, da mesma forma que o PIX.

### Referência oficial

Para números de cartão atualizados (a Mercado Pago pode alterá-los), consulte a [documentação oficial de cartões de teste](https://www.mercadopago.com.br/developers/pt/docs/checkout-api/testing).

---

## Status do projeto

Em evolução 🚀

**Próximos passos:**
- Integração com gateway de pagamento (Stripe)
- Deploy em produção com PostgreSQL
- Cobrança recorrente automática das assinaturas

---

## Autor

**Guilherme Silva**
