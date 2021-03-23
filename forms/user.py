import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from .const import HASH_METHOD
from retail.utils.tools import ts_to_datetime_str,get_uuid5
from retail.models.user import NativeUser

class User:
    def __init__(self,username=None, password=None, phone_number=None, uid=None, active=None,
        create_time=None, update_time=None, native=None):
        self.username = username
        self.password =password
        self.phone_number = phone_number
        self.uid = uid
        self.create_time = create_time
        self.update_time = update_time
        self.active = active
        self.native = native


def generate_password(password: str) -> str:
    return generate_password_hash(
        password, method=HASH_METHOD)
        
async def create_native_user(**data):
    username = data.get("username") 
    user = NativeUser(**data)
    ok,err = await user.where(conditions=("username",), requirements=(user.get("username"),), operators=("=",), columns=("id",))
    if err:
        return None,err
    if ok:
        return None,"user existed."
    if username and data.get("password"):
        data['password'] = generate_password(data.pop('password')).split(":")[-1]
        (_now := ts_to_datetime_str())
        data["create_time"] = _now
        data["update_time"] = _now
        data["active"] = 1
        data["uid"] = get_uuid5(data.get("username"))
        user.update(data)
        #return primary id
        user_id,err = await NativeUser(**data).create()

        if user_id:
            result = {
            "use_id": user_id,
            }
            return result,None
        else:
            return None,err
    else:
        return None,"username and password are required."


async def validate_login(username: str, password: str) -> "Tuple[bool, Union[User, None]]":
    #wait come make it.
    ok,err = await NativeUser(username=username).where(conditions=("username",), requirements=(username,), operators=("=",), columns=("password","uid","active","username"))
    # import pdb
    # pdb.set_trace()
    if err:

        return None,"Validate login cause a server error."
    if not ok:
        return None,"Username is incorrect."
    user = ok[0]
    if check_password_hash('{}:{}'.format(HASH_METHOD,user.pop("password")), password):  # type: ignore
        return user,None
    return None, "Password authenticate failed."