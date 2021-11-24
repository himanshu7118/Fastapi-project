from fastapi import APIRouter,HTTPException,Depends,WebSocket
from fastapi.security import APIKeyHeader
from . import models,schemas
import tortoise
import jwt,datetime
from config.settings import settings

router = APIRouter(prefix='/user')

@router.post("/",status_code=201,tags=["user"])
async def create_user(data:models.UserIn):
    user_obj = await models.User.create(**data.dict(exclude_unset=True))
    return {"status":"success","msg":"user created","data": await models.UserOut.from_tortoise_orm(user_obj)}

@router.post("/login",tags=["login"])
async def login(data: schemas.LoginSchema):
    try:
        user = await models.User.get(username=data.dict()['username'])
        if not user.check_password(data.dict()['password']):
            raise HTTPException(detail="unauthorised access",status_code=401)
        payload = {"id":user.id,"username":user.username,"type":"bearer","exp":datetime.datetime.utcnow()+settings.EXPIRATION_TIME}
        token = jwt.encode(payload,settings.SECRET_KEY,'HS256')
        return {"token":token}
    except tortoise.exceptions.DoesNotExist:
        raise HTTPException(detail="unauthorised access",status_code=401)


token = APIKeyHeader(name="Authorization",scheme_name="Bearer JWT Token")

async def authentication(token= Depends(token)):
    try:
        if token is None:
            raise HTTPException(detail="unauthorised user",status=401)
        prefix, value = token.split()
        if prefix != "Bearer":
            raise HTTPException(detail="unauthorised user",status=401)
        payload = jwt.decode(value,settings.SECRET_KEY,'HS256')
        user = await models.User.get(id=payload['id'])
        return user
    except (ValueError,tortoise.exceptions.DoesNotExist,jwt.ExpiredSignatureError):
        raise HTTPException(detail="unauthorised user",status=401)

        

@router.get("/about",tags=["user"])
async def about_page(user = Depends(authentication)):
    return {"status":"success", "msg":"about page"}

@router.get("/",tags=["user"])
async def get_user_details(user = Depends(authentication)):
    return {"status":"success", "msg":"user page","user":user}














