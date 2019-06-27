import peewee as pw
proxy = pw.Proxy()


class Job(pw.Model):
    number = pw.CharField()

    class Meta:
        database = proxy


class Invoice(pw.Model):
    number = pw.CharField()

    class Meta:
        database = proxy


class Lineitem(pw.Model):
    invoice = pw.ForeignKeyField(Invoice, backref='lineitems')
    name = pw.CharField()
    amount = pw.FloatField()

    class Meta:
        database = proxy

class Book(pw.Model):
    author = pw.CharField()
    title = pw.CharField()
    class Meta:
        database = proxy