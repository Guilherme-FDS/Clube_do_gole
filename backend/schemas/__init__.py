from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Helpers ────────────────────────────────────────────────────────────────────

Plano = Annotated[str, Field(pattern="^(mensal|semestral|anual)$")]
TipoProduto = Annotated[str, Field(pattern="^(gold|premium)$")]
StatusCupom = Annotated[str, Field(pattern="^(ativo|inativo)$")]


# ── Auth ───────────────────────────────────────────────────────────────────────

class LoginIn(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)
    guest_carrinho: list[dict] = Field(default_factory=list)


class CadastroIn(BaseModel):
    cpf: str = Field(min_length=11, max_length=14)
    nome: str = Field(min_length=1, max_length=100)
    sobrenome: str = Field(min_length=1, max_length=100)
    data_nascimento: date
    email: EmailStr
    senha: str = Field(min_length=6)
    telefone: str = Field(min_length=8, max_length=20)


class UsuarioOut(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    cpf: str
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    criado_em: datetime

    model_config = {"from_attributes": True}


class TokenOut(BaseModel):
    token: str
    tipo: str
    nome: str
    itens_migrados: int = 0


class EsqueceuSenhaIn(BaseModel):
    email: EmailStr


class RedefinirSenhaIn(BaseModel):
    token: str = Field(min_length=1)
    nova_senha: str = Field(min_length=6)


# ── Endereços ──────────────────────────────────────────────────────────────────

class EnderecoIn(BaseModel):
    tipo: str = Field(default="residencial", max_length=30)
    cep: str = Field(min_length=8, max_length=10)
    endereco: str = Field(min_length=1, max_length=255)
    numero: str = Field(min_length=1, max_length=20)
    complemento: Optional[str] = Field(default=None, max_length=100)
    bairro: str = Field(min_length=1, max_length=100)
    cidade: str = Field(min_length=1, max_length=100)
    estado: str = Field(min_length=2, max_length=2)
    pais: str = Field(default="Brasil", max_length=50)
    principal: bool = False


class EnderecoOut(BaseModel):
    id: int
    id_cliente: int
    tipo: str
    cep: str
    endereco: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    pais: str
    principal: bool
    criado_em: datetime

    model_config = {"from_attributes": True}


# ── Produtos ───────────────────────────────────────────────────────────────────

class ProdutoIn(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    tipo: TipoProduto
    descricao: Optional[str] = None
    preco: Decimal = Field(ge=0, decimal_places=2)
    imagem: Optional[str] = None
    estoque: int = Field(ge=0, default=0)
    ativo: bool = True


class ProdutoOut(BaseModel):
    id: int
    nome: str
    tipo: str
    descricao: Optional[str] = None
    preco: Decimal
    imagem: Optional[str] = None
    estoque: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}


# ── Cupons ─────────────────────────────────────────────────────────────────────

class CupomIn(BaseModel):
    codigo: str = Field(min_length=1, max_length=50)
    desconto_percentual: Decimal = Field(ge=0, le=100, decimal_places=2)
    usos_maximos: int = Field(ge=1, default=1)
    status: StatusCupom = "ativo"

    @field_validator("codigo", mode="after")
    @classmethod
    def uppercase_codigo(cls, v: str) -> str:
        return v.upper()


class CupomOut(BaseModel):
    id: int
    codigo: str
    desconto_percentual: Decimal
    usos_maximos: int
    usos_restantes: int
    status: str
    criado_em: datetime

    model_config = {"from_attributes": True}


class ValidarCupomIn(BaseModel):
    codigo: str


class ValidarCupomOut(BaseModel):
    valido: bool
    mensagem: str
    desconto: float = 0.0


# ── Carrinho ───────────────────────────────────────────────────────────────────

class AdicionarItemIn(BaseModel):
    produto_id: int = Field(gt=0)
    plano: Plano = "mensal"
    quantidade: int = Field(ge=1, default=1)


class AtualizarQuantidadeIn(BaseModel):
    item_id: int = Field(gt=0)
    quantidade: int = Field(ge=1)


class ItemCarrinhoOut(BaseModel):
    id: int
    id_produto: Optional[int] = None
    nome_produto: str
    descricao: Optional[str] = None
    plano: str
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal
    status: str

    model_config = {"from_attributes": True}


class CarrinhoOut(BaseModel):
    itens: list[ItemCarrinhoOut]
    total: float


class FinalizarIn(BaseModel):
    ids: list[int] = Field(min_length=1)
    cupom: str = ""
    desconto_cupom: float = Field(ge=0, le=100, default=0.0)


# ── Vendas ─────────────────────────────────────────────────────────────────────

class ItemVendaOut(BaseModel):
    id_produto: Optional[int] = None
    nome_produto: str
    quantidade: int
    plano: str
    valor_unitario: Decimal
    valor_total: Decimal
    imagem: Optional[str] = None
    desconto_recorrencia: float = 0.0


class PedidoOut(BaseModel):
    id: int
    data: datetime
    valor_total: Decimal
    valor_sem_desconto: Decimal
    desconto_aplicado: Decimal
    cupom_aplicado: Optional[str] = None
    economia: float
    itens: list[ItemVendaOut]


# ── Configurações ──────────────────────────────────────────────────────────────

class AtualizarPerfilIn(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    sobrenome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    telefone: str = Field(min_length=8, max_length=20)
    data_nascimento: Optional[date] = None


class AlterarSenhaIn(BaseModel):
    senha_atual: str = Field(min_length=1)
    nova_senha: str = Field(min_length=6)


# ── Admin — Clientes ───────────────────────────────────────────────────────────

class ClienteAdminOut(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    cpf: str
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    criado_em: datetime

    model_config = {"from_attributes": True}


class ClienteDetalheAdminOut(BaseModel):
    cliente: ClienteAdminOut
    enderecos: list[EnderecoOut]
    pedidos: list[dict]