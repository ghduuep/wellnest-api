from pydantic import BaseModel
from datetime import date

class EnderecoBase(BaseModel):
    rua: str
    numero: int
    complemento: str | None = None
    bairro: str
    cidade: str
    estado: str
    cep: str

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoUpdate(BaseModel):
    rua: str | None = None
    numero: int | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None

class EnderecoRead(EnderecoBase):
    id: int

class AlunoBase(BaseModel):
    nome: str
    sobrenome: str
    cpf: str
    telefone: str
    endereco: EnderecoBase | None = None
    data_nascimento: date | None = None

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: str | None = None
    sobrenome: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    endereco: EnderecoUpdate | None = None
    data_nascimento: date | None = None

class AlunoRead(AlunoBase):
    id: int