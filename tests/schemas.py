from marshmallow_peewee import ModelSchema
from .models import Job


class JobSchema(ModelSchema):
    class Meta:
        model = Job
