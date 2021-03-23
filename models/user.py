
from .simpleorm import my

class NativeUser(my.Model):#model实例类的子类

    class Meta:
        table = 'native_user'

    username = my.StringField(fixed=True,max_length=32,notnull=True)
    password = my.StringField(fixed=True,max_length=32,notnull=True)
    active = my.IntegerField(tiny=True,max_length=1)
    phone_number = my.StringField(fixed=True,max_length=20)
    create_time  = my.DatetimeField()
    update_time  = my.DatetimeField()
    uid = my.StringField(fixed=True,max_length=36)

