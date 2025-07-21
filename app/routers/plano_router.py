from fastapi import APIRouter, HTTPException
from app.dtos.plano_dto import PlanoCreate, PlanoUpdate, PlanoRead
from app.models.plano import Plano

router = APIRouter(prefix="/planos", tags=["Planos"])

@router.get('/', response_model=list[PlanoRead])
async def listar_planos():
    planos = await Plano.all()
    return [
        PlanoRead(
            id=plano.id,
            nome=plano.nome,
            descricao=plano.descricao,
            valor=plano.valor,
            duracao=plano.duracao_meses
        ) for plano in planos
    ]

@router.get('/{plano_id}', response_model=PlanoRead)
async def obter_plano(plano_id: int):
    plano = await Plano.get_or_none(id=plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    
    return PlanoRead(
        id=plano.id,
        nome=plano.nome,
        descricao=plano.descricao,
        valor=plano.valor,
        duracao=plano.duracao_meses
    )

@router.post('/', response_model=PlanoRead)
async def criar_plano(plano: PlanoCreate):
    novo_plano = Plano(
        nome=plano.nome,
        descricao=plano.descricao,
        valor=plano.valor,
        duracao=plano.duracao_meses
    )
    await novo_plano.save()
    
    return PlanoRead(
        id=novo_plano.id,
        nome=novo_plano.nome,
        descricao=novo_plano.descricao,
        valor=novo_plano.valor,
        duracao=novo_plano.duracao_meses
    )

@router.put('/{plano_id}', response_model=PlanoRead)
async def atualizar_plano(plano_id: int, plano: PlanoUpdate):
    plano_existente = await Plano.get_or_none(id=plano_id)
    if not plano_existente:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    
    plano_existente.nome = plano.nome
    plano_existente.descricao = plano.descricao
    plano_existente.valor = plano.valor
    plano_existente.duracao_meses = plano.duracao_meses
    await plano_existente.save()
    
    return PlanoRead(
        id=plano_existente.id,
        nome=plano_existente.nome,
        descricao=plano_existente.descricao,
        valor=plano_existente.valor,
        duracao=plano_existente.duracao_meses
    )

@router.delete('/{plano_id}')
async def excluir_plano(plano_id: int):
    plano = await Plano.get_or_none(id=plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    
    await plano.delete()
    return {"detail": "Plano excluído com sucesso"}