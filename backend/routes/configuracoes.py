from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_db
from repositories import auth_repo, endereco_repo
from services import venda_service
from schemas import AtualizarPerfilIn, AlterarSenhaIn, EnderecoIn, EnderecoOut, UsuarioOut
from utils.auth import login_required

router = APIRouter(prefix="/api/configuracoes", tags=["configuracoes"])

@router.get("/perfil")
async def perfil(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    cliente = await auth_repo.buscar_cliente(db, payload["id"])
    if not cliente:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    enderecos = await endereco_repo.listar(db, payload["id"])
    pedidos = await venda_service.pedidos_do_usuario(db, payload["id"])
    return {"usuario": UsuarioOut.model_validate(cliente), "enderecos": [EnderecoOut.model_validate(e) for e in enderecos], "pedidos": pedidos}

@router.put("/perfil", response_model=UsuarioOut)
async def atualizar_perfil(body: AtualizarPerfilIn, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    cliente = await auth_repo.buscar_cliente(db, payload["id"])
    if not cliente:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if body.cpf:
        if cliente.cpf and body.cpf != cliente.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado. Para alterar, entre em contato com o suporte.")
        if not cliente.cpf and await auth_repo.cpf_existe(db, body.cpf):
            raise HTTPException(status_code=409, detail="CPF já cadastrado.")
    return await auth_repo.atualizar_cliente(db, payload["id"], body.model_dump())

@router.put("/senha")
async def alterar_senha(body: AlterarSenhaIn, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    sucesso, msg = await auth_repo.alterar_senha(db, payload["id"], body.senha_atual, body.nova_senha)
    if not sucesso:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@router.get("/enderecos", response_model=list[EnderecoOut])
async def listar_enderecos(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    return await endereco_repo.listar(db, payload["id"])

@router.post("/enderecos", response_model=EnderecoOut, status_code=201)
async def adicionar_endereco(body: EnderecoIn, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    return await endereco_repo.criar(db, payload["id"], body.model_dump())

@router.put("/enderecos/{endereco_id}", response_model=EnderecoOut)
async def editar_endereco(endereco_id: int, body: EnderecoIn, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    e = await endereco_repo.atualizar(db, endereco_id, payload["id"], body.model_dump())
    if not e:
        raise HTTPException(status_code=404, detail="Endereço não encontrado.")
    return e

@router.delete("/enderecos/{endereco_id}")
async def excluir_endereco(endereco_id: int, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    sucesso, msg = await endereco_repo.remover(db, endereco_id, payload["id"])
    if not sucesso:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@router.patch("/enderecos/{endereco_id}/principal")
async def definir_principal(endereco_id: int, payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    sucesso, msg = await endereco_repo.definir_principal(db, endereco_id, payload["id"])
    if not sucesso:
        raise HTTPException(status_code=404, detail=msg)
    return {"message": msg}