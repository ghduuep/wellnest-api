from .modelobase import ModeloBase
from tortoise import fields

class Endereco(ModeloBase):
    rua = fields.CharField(max_length=255)
    numero = fields.CharField(max_length=10)
    complemento = fields.CharField(max_length=100, null=True)
    bairro = fields.CharField(max_length=100)
    cidade = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=2)
    cep = fields.CharField(max_length=10)

class Aluno(ModeloBase):
    nome = fields.CharField(max_length=100)
    sobrenome = fields.CharField(max_length=100)
    cpf = fields.CharField(max_length=11, unique=True)
    telefone = fields.CharField(max_length=15)
    endereco = fields.ForeignKeyField('models.Endereco', related_name='alunos', null=True)
    data_nascimento = fields.DateField(null=True)