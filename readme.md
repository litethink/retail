<!-- run containers -->

docker-compose up

<!-- run server -->

python app.py



<!-- client -->

import requests

data = '{"username":"user1","password":"1234"}'


<!-- register -->
data = '{"username":"huang","password":"1234"}'
<!-- #data in request.json -->
ar = requests.post("http://127.0.0.1:8000/account/register",data=data)
print(ar.json())

<!-- login -->
a = requests.post("http://127.0.0.1:8000/auth",data=data)



rt = a.json().get("refresh_token")
jwt = a.json().get("access_token")


<!-- #"cookie_set" : True, -->
a1 = requests.post("http://127.0.0.1:8000/auth/refresh",cookies=a.cookies
)
b1 = requests.get("http://127.0.0.1:8000/auth/verify",cookies=a.cookies) 
c1 = requests.get("http://127.0.0.1:8000/info",cookies=a.cookies)




<!-- "cookie_set" : False,
"authorization_header":"authorization",
"authorization_header_prefix":"Retail" -->
a2 = requests.post("http://localhost:8000/auth/refresh",data='{"refresh_token":"%s"}'%rt
,headers = {"authorization": "Retail %s"%at}
)
b2 = requests.get("http://127.0.0.1:8000/auth/verify",headers = {"authorization": "Retail %s"%jwt}) 
c2 = requests.get("http://127.0.0.1:8000/info",headers = {"authorization": "Retail %s"%jwt})



<!-- class RefreshEndpoint(BaseEndpoint):
    async def post(self, request, *args, **kwargs):
        request, args, kwargs = await self.do_incoming(request, args, kwargs)

        # TODO:
        # - Add more exceptions
        payload = await self.instance.auth.extract_payload(
            request, verify=False
        )

        try:
            #error is here
            user = await utils.call(                       #bug here need delete variable name payload 
                self.instance.auth.retrieve_user, request, payload=payload
            )
 -->