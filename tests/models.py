import peewee as pw
proxy = pw.Proxy()

class Job(pw.Model):
    class Meta:
        database = proxy
        
    number = pw.CharField()
