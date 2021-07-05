
class Field(object):
 
    def __init__(self, column_type,**kwargs):
        '''
        1，删除了参数name，field参数全部为定义字段类型相关参数，和众多有名的orm相同
        2，使用反射，方便字段的扩展，如本例使用deafault就是反射的应用
        3，由于子类属性未定义，通过kwargs传递定义子类的属性
        '''

        self.column_type = column_type #字段长度
        self.default=None  #字段默认值，如果想扩展可以填写更多的参数
        self.notnull = False
        if kwargs:
            for k,v in kwargs.items():
                if not hasattr(self,k):
                    setattr(self,k,v)
 
    def __str__(self):
        return '<%s>' % (self.__class__.__name__)
    
class StringField(Field):
 
    def __init__(self,max_length=None,fixed=True,**kwargs):
        self.max_length = max_length
        self.fixed = fixed
        if self.fixed:
            (_type := "CHAR")
        else:
            (_type := "VARCHAR")
        if self.max_length:
            (column_type := "{}({})".format(_type,self.max_length))
        else:
            (column_type := _type)
        super().__init__(column_type=column_type,**kwargs)
 

class IntegerField(Field):

    def __init__(self,max_length=None,tiny=True,**kwargs):
        self.max_length = max_length
        self.tiny = tiny
        if self.tiny:
            (_type := "TINYINT")
        else:
            (_type := "INT")
        if self.max_length:
            (column_type := "{}({})".format(_type,self.max_length))
        else:
            (column_type := _type)
        super().__init__(column_type=column_type,**kwargs)

class FloatField(Field):
    def __init__(self,max_length=None,**kwargs):
        self.max_length = max_length
        if self.max_length:
            (column_type := "FLOAT({})".format(self.max_length))
        else:
            (column_type := "FLOAT")
        super().__init__(column_type=column_type,**kwargs) 

class DatetimeField(Field):
    def __init__(self,**kwargs):
        (column_type := "DATETIME")
        super().__init__(column_type,**kwargs) 


class ModelMetaclass(type):
 
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        mappings = dict()
        for k, v in attrs.items():
            #print('k={},v={}'.format(k,v))
            if isinstance(v, Field):
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = attrs.get('Meta').table or name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)









__all__ = []
for attr in dir():
    if attr[0] != "_" and attr != "Field":
        __all__.append(attr)
