from fastapi import APIRouter, HTTPException
from app.dtos.matricula_dto import MatriculaCreate, MatriculaRead, MatriculaUpdate, StatusChoices
from app.models.matricula import Matricula

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

@router.get('/', response_model=list[MatriculaRead])
async def listar_matriculas():
    matriculas = await Matricula.all()
    return [
        MatriculaRead(
            id=matricula.id,
            aluno_id=matricula.aluno,
            plano_id=matricula.plano,
            status=matricula.status
        )
        for matricula in matriculas
    ]

@router.get('/{matricula_id}', response_model=MatriculaRead)
async def obter_matricula(matricula_id: int):
    matricula = await Matricula.get_or_none(id=matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    
    return MatriculaRead(
        id=matricula.id,
        aluno_id=matricula.aluno,
        plano_id=matricula.plano,
        status=matricula.status
    )

@router.post('/', response_model=MatriculaRead)
async def criar_matricula(matricula: MatriculaCreate):
    novo_matricula = Matricula(
        aluno=matricula.aluno_id,
        plano=matricula.plano_id,
        status=matricula.status
    )
    await novo_matricula.save()
    return MatriculaRead(
        id=novo_matricula.id,
        aluno_id=novo_matricula.aluno,
        plano_id=novo_matricula.plano,
        status=novo_matricula.status
    )

@router.patch('/{matricula_id}', response_model=MatriculaRead)
async def atualizar_matricula(matricula_id: int, matricula: MatriculaUpdate):
    existing_matricula = await Matricula.get_or_none(id=matricula_id)
    if not existing_matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    
    if matricula.status is not None:
        existing_matricula.status = matricula.status
    
    await existing_matricula.save()
    return MatriculaRead(
        id=existing_matricula.id,
        aluno_id=existing_matricula.aluno,
        plano_id=existing_matricula.plano,
        status=existing_matricula.status
    )

@router.delete('/{matricula_id}', response_model=dict)
async def excluir_matricula(matricula_id: int):
    matricula = await Matricula.get_or_none(id=matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    
    await matricula.delete()
    return {"detail": "Matrícula excluída com sucesso"}