from pydantic import BaseModel

class PlanoBase(BaseModel):
    nome: str
    descricao: str | None = None
    valor: float
    duracao_meses: int
    ativo: bool = True

class PlanoCreate(PlanoBase):
    pass

class PlanoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    valor: float | None = None
    duracao_meses: int | None = None
    ativo: bool | None = None

class PlanoRead(PlanoBase):
    id: int