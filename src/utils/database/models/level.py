"""
Level model.
"""

# Pip
from tortoise import fields
from tortoise.models import Model


class Level(Model):
    """Level table class."""

    id = fields.IntField(pk=True)
    snowflake = fields.TextField(required=True)
    guild = fields.TextField(required=True)
    experience = fields.IntField(null=False, default=0)
    level = fields.IntField(null=False, default=1)
    last_message = fields.DatetimeField(auto_now=True)

    class Meta:
        """Model metadata"""
        table = 'levels'

    def __str__(self) -> str:
        return str(self.level)
