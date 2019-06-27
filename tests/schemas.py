from marshmallow_peewee import ModelSchema, Related
from .models import Job, Invoice, Lineitem, Book


class JobSchema(ModelSchema):
    class Meta:
        model = Job

class InvoiceSchema(ModelSchema):
    lineitems = Related()
    class Meta:
        model = Invoice

class LineitemSchema(ModelSchema):
    invoice = Related()
    class Meta:
        model = Lineitem

class BookSchema(ModelSchema):
    class Meta:
        model = Book