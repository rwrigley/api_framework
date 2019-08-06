import json
from unittest import mock

from playhouse import test_utils

from api_framework.controllers import ListAPIController, RetrieveAPIController

from .models import Invoice, Lineitem, proxy, Book
from .schemas import InvoiceSchema, LineitemSchema, BookSchema


def test_fk(build_test_client, bind_models):
    bind_models(Lineitem, Invoice)
    class LineitemController(ListAPIController):
        modelselect = Lineitem
        schema_class = LineitemSchema
        prefetch = (Invoice, )

    client = build_test_client({'/lineItems': LineitemController()})

    Lineitem.create(invoice=Invoice.create(number='1'), name='Foo', amount=432)
    Lineitem.create(invoice=Invoice.create(number='2'), name='Bar', amount=200)


    with test_utils.count_queries() as counter:
        results = client.simulate_get('/lineItems').json
        assert len(results) == 2
        foo = next(r for r in results if r['name'] == 'Foo')
        assert foo
        assert foo['amount'] == 432
        assert foo['invoice']['number'] == '1'

    assert counter.count == 2



def test_list_fk(build_test_client, bind_models):
    bind_models(Lineitem, Invoice)

    class InvoiceController(RetrieveAPIController):
        modelselect = Invoice
        schema_class = InvoiceSchema
        prefetch = (Lineitem,)

    invoice = Invoice.create(number='123')
    Lineitem.create(invoice=invoice, name='Sproket', amount=1.23)
    Lineitem.create(invoice=invoice, name='Gear', amount=2.00)
    Lineitem.create(invoice=invoice, name='Shaft', amount=3.00)
    Lineitem.create(invoice=invoice, name='Lever', amount=4.00)

    client = build_test_client({'/invoice/{id}': InvoiceController()})

    with test_utils.count_queries() as counter:
        results = client.simulate_get(f'/invoice/{invoice.id}').json
        assert results['number'] == '123'
        assert isinstance(results['lineitems'], list)
        lineitems = results['lineitems']
        assert len(lineitems) == 4
        assert lineitems[0]['name'] == 'Sproket'
    assert counter.count == 2


def test_multi_field_lookup(build_test_client, bind_models):
    bind_models(Book)

    class BookController(RetrieveAPIController):
        modelselect = Book
        schema_class = BookSchema

        def get_object(self, req, title, author):
            return Book.select().where(Book.title==title, Book.author==author).get()

    book = Book.create(title='Foo', author='Bar')
    client = build_test_client({'/book/{author}/{title}': BookController()})
    results = client.simulate_get(f'/book/Bar/Foo').json
    assert results
    assert results['title'] == 'Foo'
    assert results['author'] == 'Bar'
