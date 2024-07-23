from pydantic import BaseModel

class ClothesBase(BaseModel):
    material: str
    type: str
    rating: float

class ClothesCreate(ClothesBase):
    link:str
    pass

class ClothesUpdate(ClothesBase):
    pass

class Clothes(ClothesBase):
    id: int
    link:str

    class Config:
        orm_mode = True
