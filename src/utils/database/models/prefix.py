"""
Prefix model.
"""

# Pip
from tortoise import fields
from tortoise.models import Model


class Prefix(Model):
    """Prefix table class."""

    id = fields.IntField(pk=True)
    prefix = fields.TextField(required=True)
    guild = fields.TextField(required=True)

    class Meta:
        """Model metadata"""
        table = 'prefixes'

    def __str__(self) -> str:
        return str(self.prefix)
