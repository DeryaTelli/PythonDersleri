from pydantic import BaseModel
class ProductPydantic(BaseModel):
    name:str
    price:float
    in_stock:bool
