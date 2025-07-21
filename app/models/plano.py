from .modelobase import ModeloBase
from tortoise import fields

class Plano(ModeloBase):
    nome = fields.CharField(max_length=100, unique=True)
    descricao = fields.TextField(null=True)
    valor = fields.DecimalField(max_digits=10, decimal_places=2)
    duracao_meses = fields.IntField()
    ativo = fields.BooleanField(default=True)