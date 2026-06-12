# database/models.py
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean, CheckConstraint, Date, ForeignKey,
    Integer, Numeric, String, Text, DateTime, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.engine import Base


class UsuarioAdm(Base):
    __tablename__ = "usuarios_adm"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False, default="admin")
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())


class UsuarioCliente(Base):
    __tablename__ = "usuarios_clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cpf: Mapped[Optional[str]] = mapped_column(String(14), nullable=True, unique=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    sobrenome: Mapped[str] = mapped_column(String(100), nullable=False)
    data_nascimento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telefone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    provider: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    provider_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    enderecos: Mapped[list["Endereco"]] = relationship(back_populates="cliente", cascade="all, delete-orphan")
    pedidos: Mapped[list["Venda"]] = relationship(back_populates="cliente")
    sessoes: Mapped[list["SessaoUsuario"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    assinaturas: Mapped[list["Assinatura"]] = relationship(back_populates="cliente")


class SessaoUsuario(Base):
    __tablename__ = "sessoes_usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios_clientes.id", ondelete="CASCADE"), nullable=False, index=True)
    token_jti: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    dispositivo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    expira_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    revogado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    usuario: Mapped["UsuarioCliente"] = relationship(back_populates="sessoes")


class Endereco(Base):
    __tablename__ = "enderecos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("usuarios_clientes.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, default="residencial")
    cep: Mapped[str] = mapped_column(String(10), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    complemento: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    pais: Mapped[str] = mapped_column(String(50), nullable=False, default="Brasil")
    principal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    cliente: Mapped["UsuarioCliente"] = relationship(back_populates="enderecos")


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    planos: Mapped[list["PlanoAssinatura"]] = relationship(back_populates="produto", cascade="all, delete-orphan")
    itens_carrinho: Mapped[list["ItemCarrinho"]] = relationship(back_populates="produto")
    itens_venda: Mapped[list["ItemVenda"]] = relationship(back_populates="produto")
    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(back_populates="produto")
    assinaturas: Mapped[list["Assinatura"]] = relationship(back_populates="produto")


class PlanoAssinatura(Base):
    __tablename__ = "planos_assinatura"
    __table_args__ = (
        CheckConstraint("recorrencia IN ('mensal', 'semestral', 'anual')", name="ck_planos_recorrencia"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_produto: Mapped[int] = mapped_column(ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False, index=True)
    recorrencia: Mapped[str] = mapped_column(String(20), nullable=False)
    preco_base: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    desconto_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    produto: Mapped["Produto"] = relationship(back_populates="planos")


class Cupom(Base):
    __tablename__ = "cupons"
    __table_args__ = (
        CheckConstraint("status IN ('ativo', 'inativo')", name="ck_cupons_status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    desconto_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    usos_maximos: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    usos_restantes: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="ativo")
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    vendas: Mapped[list["Venda"]] = relationship(back_populates="cupom")


class ItemCarrinho(Base):
    __tablename__ = "carrinho"
    __table_args__ = (
        CheckConstraint("plano IN ('mensal', 'semestral', 'anual')", name="ck_carrinho_plano"),
        CheckConstraint("status IN ('em processo', 'finalizado')", name="ck_carrinho_status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios_clientes.id", ondelete="CASCADE"), nullable=False, index=True)
    id_produto: Mapped[Optional[int]] = mapped_column(ForeignKey("produtos.id", ondelete="SET NULL"), nullable=True)
    id_plano: Mapped[Optional[int]] = mapped_column(ForeignKey("planos_assinatura.id", ondelete="SET NULL"), nullable=True)
    nome_produto: Mapped[str] = mapped_column(String(200), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    plano: Mapped[str] = mapped_column(String(20), nullable=False, default="mensal")
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    valor_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="em processo", index=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    produto: Mapped[Optional["Produto"]] = relationship(back_populates="itens_carrinho")
    usuario: Mapped["UsuarioCliente"] = relationship()
    plano_assinatura: Mapped[Optional["PlanoAssinatura"]] = relationship()


class Venda(Base):
    __tablename__ = "vendas"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pendente', 'pago', 'cancelado', 'estornado')",
            name="ck_vendas_status"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios_clientes.id", ondelete="SET NULL"), nullable=True, index=True)
    id_cupom: Mapped[Optional[int]] = mapped_column(ForeignKey("cupons.id", ondelete="SET NULL"), nullable=True)
    id_endereco_entrega: Mapped[Optional[int]] = mapped_column(ForeignKey("enderecos.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pendente", index=True)
    valor_original: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    valor_desconto: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    desconto_aplicado: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    cupom_aplicado: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), index=True)

    cliente: Mapped[Optional["UsuarioCliente"]] = relationship(back_populates="pedidos")
    cupom: Mapped[Optional["Cupom"]] = relationship(back_populates="vendas")
    endereco_entrega: Mapped[Optional["Endereco"]] = relationship()
    itens: Mapped[list["ItemVenda"]] = relationship(back_populates="venda", cascade="all, delete-orphan")
    pagamentos: Mapped[list["Pagamento"]] = relationship(back_populates="venda")
    assinatura: Mapped[Optional["Assinatura"]] = relationship(back_populates="venda_origem")


class ItemVenda(Base):
    __tablename__ = "itens_venda"
    __table_args__ = (
        CheckConstraint("plano IN ('mensal', 'semestral', 'anual')", name="ck_itens_venda_plano"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_venda: Mapped[int] = mapped_column(ForeignKey("vendas.id", ondelete="CASCADE"), nullable=False, index=True)
    id_produto: Mapped[Optional[int]] = mapped_column(ForeignKey("produtos.id", ondelete="SET NULL"), nullable=True)
    id_plano: Mapped[Optional[int]] = mapped_column(ForeignKey("planos_assinatura.id", ondelete="SET NULL"), nullable=True)
    nome_produto: Mapped[str] = mapped_column(String(200), nullable=False)
    plano: Mapped[str] = mapped_column(String(20), nullable=False, default="mensal")
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    valor_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    venda: Mapped["Venda"] = relationship(back_populates="itens")
    produto: Mapped[Optional["Produto"]] = relationship(back_populates="itens_venda")
    plano_assinatura: Mapped[Optional["PlanoAssinatura"]] = relationship()


class Assinatura(Base):
    __tablename__ = "assinaturas"
    __table_args__ = (
        CheckConstraint("status IN ('ativa', 'pausada', 'cancelada', 'expirada')", name="ck_assinaturas_status"),
        CheckConstraint("plano IN ('mensal', 'semestral', 'anual')", name="ck_assinaturas_plano"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("usuarios_clientes.id", ondelete="CASCADE"), nullable=False, index=True)
    id_venda_origem: Mapped[Optional[int]] = mapped_column(ForeignKey("vendas.id", ondelete="SET NULL"), nullable=True)
    id_produto: Mapped[Optional[int]] = mapped_column(ForeignKey("produtos.id", ondelete="SET NULL"), nullable=True)
    id_plano: Mapped[Optional[int]] = mapped_column(ForeignKey("planos_assinatura.id", ondelete="SET NULL"), nullable=True)
    plano: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ativa")
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    proximo_ciclo: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    cliente: Mapped["UsuarioCliente"] = relationship(back_populates="assinaturas")
    venda_origem: Mapped[Optional["Venda"]] = relationship(back_populates="assinatura")
    produto: Mapped[Optional["Produto"]] = relationship(back_populates="assinaturas")
    plano_assinatura: Mapped[Optional["PlanoAssinatura"]] = relationship()
    pagamentos: Mapped[list["Pagamento"]] = relationship(back_populates="assinatura")


class Pagamento(Base):
    __tablename__ = "pagamentos"
    __table_args__ = (
        CheckConstraint("status IN ('pendente', 'aprovado', 'recusado', 'estornado')", name="ck_pagamentos_status"),
        CheckConstraint("metodo IN ('cartao_credito', 'pix', 'boleto', 'outro')", name="ck_pagamentos_metodo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_venda: Mapped[Optional[int]] = mapped_column(ForeignKey("vendas.id", ondelete="SET NULL"), nullable=True, index=True)
    id_assinatura: Mapped[Optional[int]] = mapped_column(ForeignKey("assinaturas.id", ondelete="SET NULL"), nullable=True, index=True)
    metodo: Mapped[str] = mapped_column(String(30), nullable=False, default="pix")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pendente", index=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    gateway_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    gateway_resposta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pago_em: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    venda: Mapped[Optional["Venda"]] = relationship(back_populates="pagamentos")
    assinatura: Mapped[Optional["Assinatura"]] = relationship(back_populates="pagamentos")


class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"
    __table_args__ = (
        CheckConstraint("tipo IN ('entrada', 'saida', 'ajuste')", name="ck_estoque_tipo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_produto: Mapped[int] = mapped_column(ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(10), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    saldo_anterior: Mapped[int] = mapped_column(Integer, nullable=False)
    saldo_posterior: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    id_venda: Mapped[Optional[int]] = mapped_column(ForeignKey("vendas.id", ondelete="SET NULL"), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    produto: Mapped["Produto"] = relationship(back_populates="movimentacoes")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios_clientes.id", ondelete="CASCADE"), nullable=False, index=True)
    token: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    usado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())