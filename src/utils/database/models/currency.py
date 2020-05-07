"""
Currency model.
"""

# Pip
from tortoise import fields
from tortoise.models import Model


class Currency(Model):
    """Currency table class."""

    id = fields.IntField(pk=True)
    snowflake = fields.TextField(required=True)
    guild = fields.TextField(required=True)
    amount = fields.IntField(required=True)

    class Meta:
        """Model metadata"""
        table = 'balances'

    def __str__(self) -> str:
        return str(self.amount)
