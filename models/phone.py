from pydantic import BaseModel


class Phone(BaseModel):
    area_code: int
    phone_number: int
    type: str

    class Config:
        orm_mode = True

    @staticmethod
    def from_model(model):
        return Phone(
            area_code = int(model.area_code),
            phone_number = int(model.phone_number),
            type = str(model._type)
        )    