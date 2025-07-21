from fastapi import APIRouter, HTTPException
from app.dtos.aluno_dto import AlunoCreate, AlunoUpdate, AlunoRead, EnderecoCreate, EnderecoUpdate, EnderecoRead
from app.models.aluno import Aluno, Endereco

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get('/', response_model=list[AlunoRead])
async def listar_alunos():
    alunos = await Aluno.all().prefetch_related('endereco')
    return [
        AlunoRead(
            id=aluno.id,
            nome=aluno.nome,
            sobrenome=aluno.sobrenome,
            cpf=aluno.cpf,
            telefone=aluno.telefone,
            endereco=EnderecoRead(
                id=aluno.endereco.id,
                rua=aluno.endereco.rua,
                numero=aluno.endereco.numero,
                bairro=aluno.endereco.bairro,
                cidade=aluno.endereco.cidade,
                estado=aluno.endereco.estado,
                cep=aluno.endereco.cep
        ) if aluno.endereco else None,
            data_nascimento=aluno.data_nascimento
        ) for aluno in alunos
    ]

@router.get('/{aluno_id}', response_model=AlunoRead)
async def obter_aluno(aluno_id: int):
    aluno = await Aluno.get_or_none(id=aluno_id).prefetch_related('endereco')
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    return AlunoRead(
        id=aluno.id,
        nome=aluno.nome,
        sobrenome=aluno.sobrenome,
        cpf=aluno.cpf,
        telefone=aluno.telefone,
        endereco=EnderecoRead(
            id=aluno.endereco.id,
            rua=aluno.endereco.rua,
            numero=aluno.endereco.numero,
            bairro=aluno.endereco.bairro,
            cidade=aluno.endereco.cidade,
            estado=aluno.endereco.estado,
            cep=aluno.endereco.cep
        ),
        data_nascimento=aluno.data_nascimento
    )

@router.post('/', response_model=AlunoRead)
async def criar_aluno(aluno: AlunoCreate):
    endereco_obj = None
    if aluno.endereco:
        endereco_obj = await Endereco.create(
            rua=aluno.endereco.rua,
            numero=aluno.endereco.numero,
            complemento=aluno.endereco.complemento,
            bairro=aluno.endereco.bairro,
            cidade=aluno.endereco.cidade,
            estado=aluno.endereco.estado,
            cep=aluno.endereco.cep
        )
    novo_aluno = await Aluno.create(
        nome=aluno.nome,
        sobrenome=aluno.sobrenome,
        cpf=aluno.cpf,
        telefone=aluno.telefone,
        endereco=endereco_obj,
        data_nascimento=aluno.data_nascimento
    )
    await novo_aluno.fetch_related('endereco')
    
    return AlunoRead(
        id=novo_aluno.id,
        nome=novo_aluno.nome,
        sobrenome=novo_aluno.sobrenome,
        cpf=novo_aluno.cpf,
        telefone=novo_aluno.telefone,
        endereco=EnderecoRead(
            id=novo_aluno.endereco.id,
            rua=novo_aluno.endereco.rua,
            numero=novo_aluno.endereco.numero,
            bairro=novo_aluno.endereco.bairro,
            cidade=novo_aluno.endereco.cidade,
            estado=novo_aluno.endereco.estado,
            cep=novo_aluno.endereco.cep
        ),
        data_nascimento=novo_aluno.data_nascimento
    )

@router.patch('/{aluno_id}', response_model=AlunoRead)
async def atualizar_aluno(aluno_id: int, aluno: AlunoUpdate):
    aluno_existente = await Aluno.get_or_none(id=aluno_id).prefetch_related('endereco')
    if not aluno_existente:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    dados_atualizados = aluno.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        if campo != "endereco":
            setattr(aluno_existente, campo, valor)
    
    if 'endereco' in dados_atualizados:
        if aluno_existente.endereco:
            endereco_atualizado = EnderecoUpdate(**dados_atualizados['endereco'])
            await aluno_existente.endereco.update_from_dict(endereco_atualizado.model_dump(exclude_unset=True))
            await aluno_existente.endereco.save()
        else:
            endereco_novo = EnderecoCreate(**dados_atualizados['endereco'])
            aluno_existente.endereco = await Endereco.create(**endereco_novo.model_dump())
    
    await aluno_existente.save()

    return AlunoRead(
        id=aluno_existente.id,
        nome=aluno_existente.nome,
        sobrenome=aluno_existente.sobrenome,
        cpf=aluno_existente.cpf,
        telefone=aluno_existente.telefone,
        endereco=EnderecoRead(
            id=aluno_existente.endereco.id,
            rua=aluno_existente.endereco.rua,
            numero=aluno_existente.endereco.numero,
            bairro=aluno_existente.endereco.bairro,
            cidade=aluno_existente.endereco.cidade,
            estado=aluno_existente.endereco.estado,
            cep=aluno_existente.endereco.cep
        ),
        data_nascimento=aluno_existente.data_nascimento
    )

@router.delete('/{aluno_id}')
async def excluir_aluno(aluno_id: int):
    aluno = await Aluno.get_or_none(id=aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    await aluno.delete()
    return {"detail": "Aluno excluído com sucesso"}
