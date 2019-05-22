# Pip
from tortoise import fields
from tortoise.models import Model


class Prefix(Model):
    id = fields.IntField(pk=True)
    prefix = fields.TextField(required=True)
    guild = fields.TextField(required=True)

    class Meta:
        table = 'prefixes'

    def __str__(self):
        return str(self.prefix)
