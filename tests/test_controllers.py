import json
from unittest import mock

from playhouse import test_utils

from api_framework.controllers import ListAPIController, RetrieveAPIController

from .models import Invoice, Lineitem, proxy, Book
from .schemas import InvoiceSchema, LineitemSchema, BookSchema


def test_fk(db):
    proxy.initialize(db)
    db.create_tables([Lineitem, Invoice])

    class LineitemController(ListAPIController):
        modelselect = Lineitem
        schema_class = LineitemSchema
        prefetch = (Invoice, )

    Lineitem.create(invoice=Invoice.create(number='1'), name='Foo', amount=432)
    Lineitem.create(invoice=Invoice.create(number='2'), name='Bar', amount=200)

    controller = LineitemController()

    req = mock.Mock()
    resp = mock.Mock()

    with test_utils.count_queries() as counter:
        controller.on_get(req, resp)
        results = json.loads(resp.body)
        assert len(results) == 2
        foo = next(r for r in results if r['name'] == 'Foo')
        assert foo
        assert foo['amount'] == 432
        assert foo['invoice']['number'] == '1'

    assert counter.count == 2


def test_list_fk(db):
    proxy.initialize(db)
    db.create_tables([Lineitem, Invoice])

    class InvoiceController(RetrieveAPIController):
        modelselect = Invoice
        schema_class = InvoiceSchema
        # prefetch = (Lineitem,)

    invoice = Invoice.create(number='123')
    Lineitem.create(invoice=invoice, name='Sproket', amount=1.23)
    Lineitem.create(invoice=invoice, name='Gear', amount=2.00)
    Lineitem.create(invoice=invoice, name='Shaft', amount=3.00)
    Lineitem.create(invoice=invoice, name='Lever', amount=4.00)

    req = mock.Mock()
    resp = mock.Mock()

    controller = InvoiceController()

    with test_utils.count_queries() as counter:
        controller.on_get(req, resp, id=invoice.id)
        results = json.loads(resp.body)
        assert results['number'] == '123'
        assert isinstance(results['lineitems'], list)
        lineitems = results['lineitems']
        assert len(lineitems) == 4
        assert lineitems[0]['name'] == 'Sproket'
    assert counter.count == 2


def test_multi_field_lookup(db):
    proxy.initialize(db)
    db.create_tables([Book])

    class BookController(RetrieveAPIController):
        modelselect = Book
        schema_class = BookSchema

        def get_object(self, req, title, author):
            return Book.select().where(Book.title==title, Book.author==author).get()

    book = Book.create(title='Foo', author='Bar')

    req = mock.Mock()
    resp = mock.Mock()

    controller = BookController()
    controller.on_get(req, resp, title='Foo', author='Bar')
    results = json.loads(resp.body)
    assert results['title'] == 'Foo'
    assert results['author'] == 'Bar'
