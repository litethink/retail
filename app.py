from sanic_jwt import protected,inject_user,exceptions
from sanic import request,response
from retail.forms.user import create_native_user
from retail.serve import server 
# from retail.redis import cache
async def register_account(request: request.Request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        raise exceptions.AuthenticationFailed('Missing username or password.')
    ok,err = await create_native_user(**request.json)
    if ok:
        data = {
            "status" : 200,
            "data" : ok,
            "msg"  :"User register success."
        }
        return response.json(data)
    else:
        raise exceptions.AuthenticationFailed(err)

@protected()  # 保护该路由，只有授权用户才能访问
async def protected_route_index(request: request.Request):
    # 从 request 中获取 payload，然后返回给前端
    payload = await request.app.auth.extract_payload(request)
    return response.json({'payloadInfo': payload})

@inject_user()  # inject user If need use user info, inject user must create retrieve_user  function
@protected()    # 保护该路由，只有授权用户才能访问
async def protected_route_info(request: request.Request, user):
    # import pdb
    # pdb.set_trace()
    if user:
        data ={'userName': user.get(b"username").decode(), "personalInfo": str(user)}
        return response.json(data)
    else:
        raise exceptions.AuthenticationFailed("Retrieve user failed,maybe user is expired authorization")
    # else:  # 进入黑名单等级之后限制查看
    #     return response.json({'userName': user.username, "personalInfo": ""})

server.add_route(register_account,"/account/register",methods=["POST"])
server.add_route(protected_route_index,"/index")
server.add_route(protected_route_info,"/info")
# server.add_route(test3,"/test3")




if __name__ == '__main__':
    server.run(debug=True)