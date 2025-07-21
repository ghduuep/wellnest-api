from .modelobase import ModeloBase
from tortoise import fields
from enum import Enum

class StatusChoices(str, Enum):
    ativo = "ativo"
    pendente = "pendente"
    cancelado = "cancelado"

class Matricula(ModeloBase):
    aluno = fields.ForeignKeyField('models.Aluno', related_name='matriculas')
    plano = fields.ForeignKeyField('models.Plano', related_name='matriculas')
    status = fields.CharEnumField(StatusChoices, default=StatusChoices.pendente)