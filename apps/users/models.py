from enum import unique
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import pbkdf2_sha256

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20,unique=True)
    full_name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password,self.password)

    def save(self,*args,**kwargs):
        if "$pbkdf2-sha256" not in self.password:
            self.password = pbkdf2_sha256.hash(self.password)
        return super(User,self).save(*args,**kwargs)

UserIn = pydantic_model_creator(User,name="UserIn",exclude_readonly=True)
UserOut = pydantic_model_creator(User,name="UserOut",exclude = ['password'])