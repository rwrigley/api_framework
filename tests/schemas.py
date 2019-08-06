from marshmallow_peewee import ModelSchema, Related
from marshmallow.fields import Nested
from .models import Job, Invoice, Lineitem, Book


class JobSchema(ModelSchema):
    class Meta:
        model = Job


class LineitemSchema(ModelSchema):
    invoice = Related()
    class Meta:
        model = Lineitem


class InvoiceSchema(ModelSchema):
    lineitems = Nested(LineitemSchema, many=True)
    class Meta:
        model = Invoice


class BookSchema(ModelSchema):
    class Meta:
        model = Book