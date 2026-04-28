-- ============================================================
-- Clube do Gole — Schema PostgreSQL
-- Substitui todos os arquivos CSV por tabelas relacionais
-- ============================================================

-- Extensão para UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- USUÁRIOS ADMINISTRADORES
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios_adm (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(150) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    senha       VARCHAR(255) NOT NULL,
    tipo        VARCHAR(20)  NOT NULL DEFAULT 'admin',
    criado_em   TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- USUÁRIOS CLIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios_clientes (
    id               SERIAL PRIMARY KEY,
    cpf              VARCHAR(14)  NOT NULL UNIQUE,
    nome             VARCHAR(100) NOT NULL,
    sobrenome        VARCHAR(100) NOT NULL,
    data_nascimento  DATE,
    email            VARCHAR(150) NOT NULL UNIQUE,
    senha            VARCHAR(255) NOT NULL,
    telefone         VARCHAR(20),
    criado_em        TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- ENDEREÇOS DOS CLIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS enderecos (
    id           SERIAL PRIMARY KEY,
    id_cliente   INTEGER      NOT NULL REFERENCES usuarios_clientes(id) ON DELETE CASCADE,
    tipo         VARCHAR(30)  NOT NULL DEFAULT 'residencial',
    cep          VARCHAR(10)  NOT NULL,
    endereco     VARCHAR(255) NOT NULL,
    numero       VARCHAR(20)  NOT NULL,
    complemento  VARCHAR(100),
    bairro       VARCHAR(100) NOT NULL,
    cidade       VARCHAR(100) NOT NULL,
    estado       VARCHAR(2)   NOT NULL,
    pais         VARCHAR(50)  NOT NULL DEFAULT 'Brasil',
    principal    BOOLEAN      NOT NULL DEFAULT FALSE,
    criado_em    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- PRODUTOS
-- ============================================================
CREATE TABLE IF NOT EXISTS produtos (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(200) NOT NULL,
    tipo        VARCHAR(20)  NOT NULL CHECK (tipo IN ('gold', 'premium')),
    descricao   TEXT,
    preco       NUMERIC(10, 2) NOT NULL DEFAULT 0,
    imagem      TEXT,               -- base64 ou URL
    estoque     INTEGER      NOT NULL DEFAULT 0,
    ativo       BOOLEAN      NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP    NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP  NOT NULL DEFAULT NOW()
);

-- ============================================================
-- CUPONS DE DESCONTO
-- ============================================================
CREATE TABLE IF NOT EXISTS cupons (
    id                   SERIAL PRIMARY KEY,
    codigo               VARCHAR(50)    NOT NULL UNIQUE,
    desconto_percentual  NUMERIC(5, 2)  NOT NULL DEFAULT 0,
    usos_maximos         INTEGER        NOT NULL DEFAULT 1,
    usos_restantes       INTEGER        NOT NULL DEFAULT 1,
    status               VARCHAR(10)    NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo')),
    criado_em            TIMESTAMP      NOT NULL DEFAULT NOW()
);

-- ============================================================
-- CARRINHO
-- ============================================================
CREATE TABLE IF NOT EXISTS carrinho (
    id_carrinho    UUID         NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    id_usuario     VARCHAR(100) NOT NULL,  -- pode ser id numérico ou "guest_<uuid>"
    id_produto     INTEGER      REFERENCES produtos(id) ON DELETE SET NULL,
    nome_produto   VARCHAR(200) NOT NULL,
    descricao      TEXT,
    plano          VARCHAR(20)  NOT NULL DEFAULT 'mensal' CHECK (plano IN ('mensal', 'semestral', 'anual')),
    quantidade     INTEGER      NOT NULL DEFAULT 1,
    valor_unitario NUMERIC(10, 2) NOT NULL DEFAULT 0,
    valor_total    NUMERIC(10, 2) NOT NULL DEFAULT 0,
    status         VARCHAR(20)  NOT NULL DEFAULT 'em processo' CHECK (status IN ('em processo', 'finalizado')),
    criado_em      TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- ============================================================
-- VENDAS / PEDIDOS
-- ============================================================
CREATE TABLE IF NOT EXISTS vendas (
    id_compra          UUID           NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    id_usuario         INTEGER        REFERENCES usuarios_clientes(id) ON DELETE SET NULL,
    id_produto         INTEGER        REFERENCES produtos(id) ON DELETE SET NULL,
    quantidade         INTEGER        NOT NULL DEFAULT 1,
    valor_original     NUMERIC(10, 2) NOT NULL DEFAULT 0,
    valor_desconto     NUMERIC(10, 2) NOT NULL DEFAULT 0,
    valor_total        NUMERIC(10, 2) NOT NULL DEFAULT 0,
    plano              VARCHAR(20)    NOT NULL DEFAULT 'mensal',
    desconto_aplicado  NUMERIC(5, 2)  NOT NULL DEFAULT 0,
    cupom_aplicado     VARCHAR(50),
    data               TIMESTAMP      NOT NULL DEFAULT NOW()
);

-- ============================================================
-- DESCONTOS POR PLANO (substitui descontos.csv)
-- ============================================================
CREATE TABLE IF NOT EXISTS descontos_plano (
    id       SERIAL PRIMARY KEY,
    plano    VARCHAR(20)   NOT NULL UNIQUE CHECK (plano IN ('mensal', 'semestral', 'anual')),
    desconto NUMERIC(5, 2) NOT NULL DEFAULT 0
);

-- ============================================================
-- ÍNDICES para performance
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_carrinho_usuario  ON carrinho(id_usuario);
CREATE INDEX IF NOT EXISTS idx_carrinho_status   ON carrinho(status);
CREATE INDEX IF NOT EXISTS idx_vendas_usuario    ON vendas(id_usuario);
CREATE INDEX IF NOT EXISTS idx_vendas_produto    ON vendas(id_produto);
CREATE INDEX IF NOT EXISTS idx_enderecos_cliente ON enderecos(id_cliente);

-- ============================================================
-- DADOS INICIAIS
-- ============================================================

-- Admin padrão (senha deve ser alterada em produção)
INSERT INTO usuarios_adm (nome, email, senha, tipo)
VALUES ('Administrador', 'admin@clubedogole.com', 'admin123', 'admin')
ON CONFLICT (email) DO NOTHING;

-- Descontos por plano de recorrência
INSERT INTO descontos_plano (plano, desconto)
VALUES
    ('mensal',    0.00),
    ('semestral', 5.00),
    ('anual',    10.00)
ON CONFLICT (plano) DO NOTHING;