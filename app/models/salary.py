from pydantic import BaseModel, Field
from typing import List, Optional, Tuple

class TaxBracket(BaseModel):
    limit: float
    rate: float

class TaxConfig(BaseModel):
    BRACKETS: List[TaxBracket]

class SalaryInput(BaseModel):
    gross_salary: float = Field(..., description="Gross salary amount")
    number_of_dependents: int = Field(..., description="Number of dependents")

class SalaryOutput(BaseModel):
    gross_salary: float
    net_salary: float
    insurance_amount: float
    personal_income_tax: float

class EmployeeData(BaseModel):
    id: int
    employee_name: str
    gross_salary: float
    number_of_dependents: int
    net_salary: Optional[float] = None

class BulkSalaryOutput(BaseModel):
    result: List[EmployeeData]

    
    