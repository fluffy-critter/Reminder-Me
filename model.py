from peewee import *

database = SqliteDatabase('reminders.db')
database.connect()

class BaseModel(Model):
    class Meta:
        database = database

    @staticmethod
    def update_schema():
        ''' do nothing '''

class Feed(BaseModel):
    # use a generated guid for the index, for mild security
    guid = CharField(null=False,unique=True)

    # title for updates
    name = CharField(null=False)

    # text to display on updates
    description = CharField()

    # time of next notification
    notify_next = DateTimeField()

    # frequency between notifications
    notify_interval = IntegerField(null=False)

    # unit of the notification interval (in seconds)
    notify_unit = IntegerField(null=False)

    # last-seen time
    last_seen = DateTimeField(null=True)

def create_tables():
    for table in [
            Feed,
            ]:
        table.create_table(fail_silently=True)
        table.update_schema()

        
