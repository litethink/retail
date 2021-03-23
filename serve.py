from sanic import Sanic
from sanic.log import logger
from sanic_redis import SanicRedis



test_config = {
    "appname" : "oops",
    "mysql" : {
        "host"  : "127.0.0.1",
        "database"    : "retail001",
        "user"    : "retail001",
        "password"    : "001retail"
        },
    "redis":{
        "cache" :{
            'address': ('127.0.0.1', 6379),
            'db': 0,
            'decode_responses' : True
        },
    },
    "jwt" :{
        "url_prefix" : '/auth',
        "secret" : ',$FCyFZ^b16#m:ragM#d-!;4!U5wdZ~ZPOI%ZDF(kkr%MaBU42AN:jXgp7',
        "expiration_delta" : 1 * 60,
        "cookie_set" : True,
        "cookie_access_token_name" : "access_token",
        "user_id" : "uid",
        "claim_iat" : True, # 显示签发时间，JWT的默认保留字段，在 sanic-jwt 中默认不显示该项   
    },
    }


class Server:
    """
    """
    def __init__(self,**kwargs):

        self.__app__ = Sanic(kwargs.pop("appname"),register=False)
        self.__logger__ = logger
        self.__app__.config.update(kwargs.pop("redis"))
        self.__cache__ = SanicRedis(self.__app__, config_name="cache")
        self.config = kwargs
        #set cache ex time, must  more 3 minute than  jwt expiration_delta
        self.cache_expiration = kwargs.get("jwt")["expiration_delta"] +10
    
    @property
    def app(self):
        return self.__app__ 

    @property
    def logger(self):
        return self.__logger__

    @property
    def cache(self):
        return self.__cache__.conn
    
    @property
    def add_route(self):
        return self.__app__.add_route

    def run(self,host="127.0.0.1",port=8000,**kwargs):
        self.__app__.run(host=host,port=port,**kwargs)


server = Server(**test_config)


