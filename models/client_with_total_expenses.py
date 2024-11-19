from pydantic import BaseModel


class ClientWithTotalExpenses(BaseModel):
    first_name: str
    last_name: str
    total_expenses: float

    @staticmethod
    def from_model(model):
        return ClientWithTotalExpenses(
            first_name=model['client'].first_name,
            last_name=model['client'].last_name,
            total_expenses=model['expenses']
        )

    class Config:
        orm_mode = True
    

