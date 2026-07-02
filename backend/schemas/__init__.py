# schemas/__init__.py
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


# ── Helpers ────────────────────────────────────────────────────────────────────

Plano = Annotated[str, Field(pattern="^(mensal|semestral|anual)$")]
StatusCupom = Annotated[str, Field(pattern="^(ativo|inativo)$")]
StatusVenda = Annotated[str, Field(pattern="^(pendente|pago|cancelado|estornado)$")]


def _validar_forca_senha(v: str) -> str:
    if len(v) < 8:
        raise ValueError("A senha deve ter no mínimo 8 caracteres.")
    if not any(c.isupper() for c in v):
        raise ValueError("A senha deve conter ao menos uma letra maiúscula.")
    if not any(c.islower() for c in v):
        raise ValueError("A senha deve conter ao menos uma letra minúscula.")
    if not any(c.isdigit() for c in v):
        raise ValueError("A senha deve conter ao menos um número.")
    return v


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
    senha: str = Field(min_length=8)
    telefone: str = Field(min_length=8, max_length=20)

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        return _validar_forca_senha(v)

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: date) -> date:
        hoje = date.today()
        idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))
        if v > hoje:
            raise ValueError("Data de nascimento não pode ser no futuro.")
        if idade > 120:
            raise ValueError("Data de nascimento inválida.")
        if idade < 18:
            raise ValueError("Cadastro permitido apenas para maiores de 18 anos.")
        return v


class OAuthCallbackIn(BaseModel):
    code: str = Field(min_length=1)
    provider: str = Field(pattern="^(google|facebook)$")
    guest_carrinho: list[dict] = Field(default_factory=list)


class UsuarioOut(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    provider: Optional[str] = None
    ativo: bool
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
    nova_senha: str = Field(min_length=8)

    @field_validator("nova_senha")
    @classmethod
    def validar_nova_senha(cls, v: str) -> str:
        return _validar_forca_senha(v)


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
    descricao: Optional[str] = None
    ativo: bool = True


class ProdutoOut(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}


# ── Planos de Assinatura ───────────────────────────────────────────────────────

class PlanoIn(BaseModel):
    recorrencia: Plano
    preco_base: Decimal = Field(gt=0, decimal_places=2)
    desconto_pct: Decimal = Field(ge=0, le=100, decimal_places=2, default=Decimal("0"))
    ativo: bool = True


class PlanoOut(BaseModel):
    id: int
    id_produto: int
    recorrencia: str
    preco_base: Decimal
    desconto_pct: Decimal
    preco_total: Decimal
    economia: Decimal
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}


class ProdutoComPlanosOut(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    ativo: bool
    planos: list[PlanoOut] = []

    model_config = {"from_attributes": True}


# ── Cupons ─────────────────────────────────────────────────────────────────────

TipoDesconto = Annotated[str, Field(pattern="^(percentual|fixo)$")]


class CupomIn(BaseModel):
    codigo: str = Field(min_length=1, max_length=50)
    tipo_desconto: TipoDesconto = "percentual"
    desconto_percentual: Decimal = Field(ge=0, le=100, decimal_places=2, default=Decimal("0"))
    desconto_fixo: Optional[Decimal] = Field(ge=0, default=None)
    usos_maximos: Optional[int] = Field(ge=1, default=None)
    valido_ate: Optional[date] = None
    status: StatusCupom = "ativo"

    @field_validator("codigo", mode="after")
    @classmethod
    def uppercase_codigo(cls, v: str) -> str:
        return v.upper()

    @model_validator(mode="after")
    def validar_desconto(self) -> "CupomIn":
        if self.tipo_desconto == "percentual" and self.desconto_percentual == 0:
            raise ValueError("Informe desconto_percentual para tipo percentual.")
        if self.tipo_desconto == "fixo" and not self.desconto_fixo:
            raise ValueError("Informe desconto_fixo para tipo fixo.")
        return self


class CupomOut(BaseModel):
    id: int
    codigo: str
    tipo_desconto: str
    desconto_percentual: Decimal
    desconto_fixo: Optional[Decimal]
    usos_maximos: Optional[int]
    usos_restantes: Optional[int]
    valido_ate: Optional[date]
    status: str
    criado_em: datetime

    model_config = {"from_attributes": True}


class ValidarCupomIn(BaseModel):
    codigo: str


class ValidarCupomOut(BaseModel):
    valido: bool
    mensagem: str
    desconto: float = 0.0          # sempre percentual equivalente para o frontend
    desconto_tipo: str = "percentual"
    desconto_fixo: Optional[float] = None


# ── Carrinho ───────────────────────────────────────────────────────────────────

class AdicionarItemIn(BaseModel):
    produto_id: int = Field(gt=0)
    plano_id: int = Field(gt=0)
    quantidade: int = Field(ge=1, default=1)


class AtualizarQuantidadeIn(BaseModel):
    item_id: int = Field(gt=0)
    quantidade: int = Field(ge=1)


class ItemCarrinhoOut(BaseModel):
    id: int
    id_carrinho: int = 0
    id_produto: Optional[int] = None
    id_plano: Optional[int] = None
    nome_produto: str
    descricao: Optional[str] = None
    plano: str
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal
    status: str

    @model_validator(mode='after')
    def set_id_carrinho(self):
        self.id_carrinho = self.id
        return self

    model_config = {"from_attributes": True}


class CarrinhoOut(BaseModel):
    itens: list[ItemCarrinhoOut]
    total: float


class FinalizarIn(BaseModel):
    ids: list[int] = Field(min_length=1)
    cupom: Optional[str] = None
    desconto_cupom: float = Field(ge=0, le=100, default=0.0)   # percentual
    desconto_fixo_cupom: Optional[float] = Field(ge=0, default=None)  # valor R$


# ── Vendas ─────────────────────────────────────────────────────────────────────

class ItemVendaOut(BaseModel):
    id_produto: Optional[int] = None
    id_plano: Optional[int] = None
    nome_produto: str
    quantidade: int
    plano: str
    valor_unitario: Decimal
    valor_total: Decimal
    imagem: Optional[str] = None
    desconto_recorrencia: float = 0.0


class PedidoOut(BaseModel):
    id: int
    status: str
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
    cpf: Optional[str] = Field(default=None, min_length=11, max_length=14)


class AlterarSenhaIn(BaseModel):
    senha_atual: str = Field(min_length=1)
    nova_senha: str = Field(min_length=8)

    @field_validator("nova_senha")
    @classmethod
    def validar_nova_senha(cls, v: str) -> str:
        return _validar_forca_senha(v)


# ── Admin — Clientes ───────────────────────────────────────────────────────────

class ClienteAdminOut(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    provider: Optional[str] = None
    ativo: bool
    criado_em: datetime

    model_config = {"from_attributes": True}


class ClienteDetalheAdminOut(BaseModel):
    cliente: ClienteAdminOut
    enderecos: list[EnderecoOut]
    pedidos: list[dict]