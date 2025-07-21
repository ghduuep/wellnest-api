from pydantic import BaseModel
from app.models.matricula import StatusChoices

class MatriculaBase(BaseModel):
    aluno_id: int
    plano_id: int
    status: StatusChoices

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaUpdate(BaseModel):
    aluno_id: int | None = None
    plano_id: int | None = None
    status: StatusChoices | None = None

class MatriculaRead(MatriculaBase):
    id: int