from pydantic import BaseModel

class ToDoItemBase(BaseModel):
    title: str
    description: str
   

class ToDoItemCreate(ToDoItemBase):
    pass

class ToDoItem(ToDoItemBase):
    id: int

    class Config:
        orm_mode = True
