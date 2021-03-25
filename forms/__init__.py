from sanic import request,response
from sanic_jwt import exceptions,Configuration,Responses,Authentication,initialize
from sanic_jwt.utils import generate_token
from retail.utils.tools import get_uuid5
from retail.serve import server
from retail.exceptions import CacheProcessFailed,RefreshTokenFailed,UnknownFailed 
from .user import validate_login

async def jwt_authenticate(request, *args, **kwargs):
    """user:str uid:str return {"usd":uid}"""
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # import pdb
    # pdb.set_trace()
    if not username or not password:
        raise exceptions.AuthenticationFailed('Missing username or password.')
    
    user, err = await validate_login(username, password)
    if not user:
        raise exceptions.AuthenticationFailed(err)
    if not user.pop("active"):  # type: ignore
        raise exceptions.AuthenticationFailed(
            'The account has been deactivated!')
    #uid in user field here.
    user_id = user.get("uid")
    #store user info to cache.
    with await server.cache as cache:
        try:
            for k in list(user):
                ok = await cache.hset(user_id,k,user.pop(k))
                await cache.expire(user_id,server.cache_expiration)
        except:
            
            CacheProcessFailed("Store user cache but failed")

    #jwt config user_id here
    return {'user_id': user_id}  # type: ignore




async def store_refresh_token(user_id, refresh_token, *args, **kwargs):
    if not user_id:
        raise RefreshTokenFailed(
        'Store refresh token but do not have user id')
    with await server.cache as cache:

        try:
            await cache.hset(user_id,"refresh_token",refresh_token)
            await cache.expire(user_id,server.cache_expiration)
        except:
            CacheProcessFailed("Store refresh token failed")
    
async def retrieve_refresh_token(request, user_id, *args, **kwargs):
    # import pdb
    # pdb.set_trace()
    if not user_id:
        raise RefreshTokenFailed(
        'Retrieve refresh token but do not have user id')
    with await server.cache as cache:
        try:
            await cache.hget(user_id,"refresh_token")
        except:
            CacheProcessFailed("Retrieve refresh token failed")
    

class jwt_config(Configuration):
    (jwt_cfg :=server.config.pop("jwt"))
    url_prefix = jwt_cfg.pop('url_prefix')
    secret     = jwt_cfg.pop('secret')
    cookie_set = jwt_cfg.pop('cookie_set')
    user_id    = jwt_cfg.pop('user_id')
    claim_iat  = jwt_cfg.pop('claim_iat')#显示签发时间，JWT的默认保留字段，在 sanic-jwt 中默认不显示该项
    cookie_access_token_name = jwt_cfg.pop('cookie_access_token_name')
    refresh_token_enabled    = jwt_cfg.pop("refresh_token_enabled")
    authorization_header     = jwt_cfg.pop("authorization_header")
    expiration_delta         = jwt_cfg.pop('expiration_delta')
    authorization_header_prefix =  jwt_cfg.pop("authorization_header_prefix")

class jwt_response(Responses):
    @staticmethod
    def exception_response(request: request.Request, exception: exceptions):
        msg = str(exception)
        if exception.status_code == 500:
            msg = str(exception)
        elif isinstance(exception, exceptions.AuthenticationFailed):
            msg = str(exception)
        else:
            if "expired" in msg:
                msg = "Expired authorization."
            else:
                msg = "No authorization."
        result = {
            "status": exception.status_code,
            "data": None,
            "msg": msg
        }
        return response.json(result, status=exception.status_code)

class User:
    def __init__(self,user_id,username):
        self.user_id = user_id
        self.username = username



class jwt_authentication(Authentication):

    # 从 payload 中解析用户信息，然后返回查找到的用户
    # args[0]: request
    # args[1]: payload

    async def retrieve_user(self, *args, **kwargs):
        user_id_attribute = self.config.user_id()
        if not args or len(args) < 2 or not args[1]:
            return {}
        if user_id_attribute not in args[1]:
            return {}
        user_id = dict(args[1]).get(user_id_attribute)

        if user_id:  
            # await self.store_refresh_token(user_id=user_id,refresh_token=get_uuid4())
            with await server.cache as cache:
                try:
                    user_b = await cache.hgetall(user_id)
                    userf = {
                     "user_id" : user_b.get(b"uid").decode(),
                     "username" : user_b.get(b"username").decode()}
                    return userf
                except:
                    CacheProcessFailed("Get user cache but failed.")
                
        else:
            return UnknownFailed("Can not retrieve user id.")


    async def extend_payload(self, payload, *args, **kwargs):
        """call after authenticate login"""
        user_id_attribute = self.config.user_id()
        user_id = payload.get(user_id_attribute)
        with await server.cache as cache:
            try:
                ok = await cache.hgetall(user_id)
            except:
                CacheProcessFailed("Get user cache but failed.")
        payload.update({'username': ok.get(b"username").decode()})  
        return payload

    async def extract_payload(self, req, verify=True, *args, **kwargs):
        return await super().extract_payload(req, verify)


initialize(server.app, authenticate=jwt_authenticate, 
           configuration_class=jwt_config, responses_class=jwt_response,authentication_class=jwt_authentication,
           store_refresh_token=store_refresh_token,retrieve_refresh_token=retrieve_refresh_token,
           generate_refresh_token=generate_token) #