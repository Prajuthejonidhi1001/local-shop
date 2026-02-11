from pydantic import BaseModel, Field, EmailStr, GetJsonSchemaHandler
from typing import List, Optional, Any
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str
    phone: Optional[str] = None
    pincode: Optional[str] = None
    shop_image: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_open: bool = True

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    sub_category: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    stock: int = 0
    images: List[str] = []
    isActive: bool = True

class ProductInDB(ProductBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    seller: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True