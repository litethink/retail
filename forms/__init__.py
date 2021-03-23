from sanic import request,response
from retail.serve import server    
from .user import validate_login
from sanic_jwt import exceptions,Configuration,Responses,Authentication,initialize

async def jwt_authenticate(request, *args, **kwargs):
    """user:str uid:str return {"usd":uid}"""
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        raise exceptions.AuthenticationFailed('Missing username or password.')
    
    user, err = await validate_login(username, password)
    if not user:
        raise exceptions.AuthenticationFailed(err)
    if not user.pop("active"):  # type: ignore
        raise exceptions.AuthenticationFailed(
            'The account has been deactivated!')
    uid = user.get("uid")
    with await server.cache as cache:
        for k in list(user):
            ok = await cache.hset(uid,k,user.pop(k))
        await cache.expire(uid,server.cache_expiration)
    # self.cache.set("")
    return {'uid': uid}  # type: ignore

class jwt_config(Configuration):
    (jwt_cfg :=server.config.pop("jwt"))
    url_prefix = jwt_cfg.pop('url_prefix')
    secret = jwt_cfg.pop('secret')
    expiration_delta = jwt_cfg.pop('expiration_delta')
    cookie_set = jwt_cfg.pop('cookie_set')
    cookie_access_token_name = jwt_cfg.pop('cookie_access_token_name')
    user_id = jwt_cfg.pop('user_id')
    claim_iat = jwt_cfg.pop('claim_iat')#显示签发时间，JWT的默认保留字段，在 sanic-jwt 中默认不显示该项


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
        with await server.cache as cache:
            user = await cache.hgetall(user_id)
            if user:
                return user
            else:
                return None

    # need change it
    async def extend_payload(self, payload, *args, **kwargs):
        # 可以获取 User 中的一些属性添加到 payload 中
        # 注意：payload 信息是公开的，这里不要添加敏感信息
        user_id_attribute = self.config.user_id()
        user_id = payload.get(user_id_attribute)
        # import pdb
        # pdb.set_trace()
        # TODO: 根据项目实际情况进行修改
        with await server.cache as cache:
            ok = await cache.hgetall(user_id)
        payload.update({'username': ok.get(b"username").decode()})  # 比如添加性别属性
        return payload

    async def extract_payload(self, req, verify=True, *args, **kwargs):
        return await super().extract_payload(req, verify)

initialize(server.app, authenticate=jwt_authenticate,authentication_class=jwt_authentication, 
           configuration_class=jwt_config, responses_class=jwt_response) #