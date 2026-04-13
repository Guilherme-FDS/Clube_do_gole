# Clube do Gole

Plataforma web de um clube de assinatura de bebidas, com sistema completo de navegação, produtos, carrinho, checkout e área administrativa.

---

## 🌐 Acesse o projeto online

👉 https://web-production-a5f51.up.railway.app

---

## Sobre o projeto

O **Clube do Gole** é um sistema web inspirado em um modelo real de negócio de assinatura de bebidas, onde o usuário pode navegar por produtos, montar pedidos e interagir com diferentes áreas da aplicação.

O projeto simula uma operação completa de e-commerce com foco em experiência do usuário e organização de dados.

---

## 🔐 Acesso ao sistema

### Área administrativa

Para acessar o painel administrativo, utilize:

- **Email:** admin@clubedogole.com.br  
- **Senha:** 1234  

### Usuário comum

Para acessar como usuário comum, basta realizar o cadastro e login normalmente pela aplicação.

---

## 🎟️ Cupons para teste

Utilize os cupons abaixo no checkout:

- **GOLE15** → Desconto promocional  
- **CLUBE10** → Desconto especial  

---

## Modelo de negócio

O sistema foi baseado em um plano real de assinatura, com:

- Planos mensais de bebidas
- Linha intermediária e premium
- Experiência personalizada para o usuário
- Possibilidade de expansão para e-commerce completo

---

## Tecnologias utilizadas

- Python (Flask)
- HTML5
- CSS3
- JavaScript
- CSV (simulação de banco de dados)

---

## Estrutura do projeto

```bash
Clube_do_gole
├── app.py
├── routes
│   └── views.py
├── templates
├── static
│   ├── css
│   ├── js
│   ├── img
│   └── data (arquivos CSV)
├── requirements.txt
└── Procfile
Funcionalidades
Sistema de navegação entre páginas (Flask)
Listagem de produtos
Carrinho de compras
Checkout
Área de login
Painel administrativo
Gestão de produtos
Sistema de cupons
Dashboard de vendas
Leitura de dados via arquivos CSV
Como executar o projeto
1. Clonar o repositório
git clone https://github.com/Guilherme-FDS/Clube_do_gole.git
cd Clube_do_gole
2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux
3. Instalar dependências
pip install -r requirements.txt
4. Rodar o projeto
python app.py

Acesse no navegador:

http://localhost:5000
Objetivo do projeto

Este projeto foi desenvolvido para praticar:

Estruturação de aplicações com Flask
Separação entre frontend e backend
Organização de rotas
Simulação de banco de dados com CSV
Construção de sistemas completos (tipo ERP / e-commerce)
Diferenciais
Projeto baseado em um modelo real de negócio
Estrutura próxima de aplicações profissionais
Backend funcional com Flask
Simulação de dados reais
Possibilidade de evolução para banco de dados real (PostgreSQL)
Próximos passos (melhorias futuras)
Integração com banco de dados (PostgreSQL)
Sistema de autenticação seguro
API REST
Integração com pagamentos
Deploy em nuvem (Render, Railway, etc)
Status do projeto

Em evolução 🚀

Autor

Guilherme Silva