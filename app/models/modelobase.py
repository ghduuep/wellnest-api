from tortoise.models import Model
from tortoise import fields

class ModeloBase(Model):
    id = fields.IntField(primary_key=True)
    criado_em = fields.DatetimeField(auto_now_add=True)
    atualizado_em = fields.DatetimeField(auto_now=True)