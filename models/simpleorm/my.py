
import sys
import functools
from sanicdb import SanicDB
from retail.serve import server
from .base import *

__db__ = SanicDB(**server.config.pop("mysql"),sanic=server.app)

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.__db__ = __db__
 
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
 
    # def __setattr__(self, key, value):
    #     self[key] = value
 
    def arrange(self):
        (fields := [])
        (params := [])
        for k, v in self.__mappings__.items():
            if not getattr(self, k,v.default):
                pass
                if v.notnull:
                    raise ValueError(r"{} assigned no null but value is None".format(k))
            else: 
                fields.append(k)
                params.append(getattr(self, k,v.default))
        return fields,params


    def single_task(self,method,*args,**kwargs):
        try:
            data =  method(*args,**kwargs)
            return data,None
        except Exception as e:
            error = e
            return None,error.__str__()

    async def query(self,*args,**kwargs):
        try:
            data = await self.__db__.query(*args,**kwargs)
            return data,None
        except Exception as e:
            error = e
            return None,error.__str__()

    async def execute(self,*args,**kwargs):
        try:
            data = await self.__db__.execute(*args,**kwargs)
            return data,None
        except Exception as e:
            error = e
            return None,error.__str__()

    async def findall(self,columns:tuple=None):
        if columns:   
            (sql := 'select {} from {};'.format(self.join_column(columns), self.__table__))
        else:
            (sql := 'select * from {};'.format(self.__table__))
        ok,err = await self.query(sql)
        return ok,err 

    async def where(self,conditions:tuple, requirements:tuple,operators:tuple,logics:tuple=(),columns:tuple=None):
        """
            when sentence make up "where x=a and y=b and z>c";
            parameter is conditions=(x,y,z),requirements=(a,b,c),operators=(=,=,>),logics=(and,and)
        """
        (length := len(conditions))
        if length == len(operators) and length == len(requirements)  and length - len(logics) == 1:
            if  length == 1:
                sentence = ' {}{}"{}"'.format(conditions[0],operators[0],(requirements[0]))
            else:
                for i in range(length-1):
                    sentence = ' {}{}"{}" {}'.format(conditions[i],operators[i],requirements[i],logics[i])
                sentence = '{} {}{}"{}"'.format(sentence,conditions[-1],operators[-1],requirements[-1])
        else:
            return None,"require strict length to make up a query sentence."
        if columns:   
            (sql := 'select {} from {} where{};'.format(self.join_column(columns), self.__table__, sentence))
        else:
            (sql := 'select * from {} where{};'.format(self.__table__, sentence))
        ok,err = await self.query(sql)
        if err:
            server.logger.error(err)
        return ok,err
   
    async def create(self):
        ok,err =  self.single_task(method=self.arrange)
        if ok:
            fields,params = ok
        else:
            return None,err
        # import pdb
        # pdb.set_trace()
        (sql := 'insert into {} ({}) values ({})'.format(self.__table__, self.join_column(fields) ,self.join_value(params)))
        ok,err = await self.execute(sql)
        if err:
            server.logger.error(err)
        return ok,err

    def join_column(self,attrs,pattern=','):
        return  functools.reduce(lambda x,y:'{}{}{}'.format(x,pattern,y),attrs)
        
    def join_value(self,attrs,pattern='","'):
        return  '"{}"'.format(functools.reduce(lambda x,y:'{}{}{}'.format(x,pattern,y),attrs))

#insert into native_user (username,password,activate,create_time,update_time,uid) values ("user1","150000$hgFmn2tN$8c749b81d59c5420528305956e0a500756b9b5b67152d29afca1bc23dc2b91c1","1","2012-01-01 15:32:31","2012-01-01 15:32:31","e063bb16-cc76-558b-9f94-afe212747cda")