from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    username = fields.TextField() 
    password_hash = fields.CharField(max_length=255)

