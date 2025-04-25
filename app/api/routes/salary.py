from fastapi import APIRouter, UploadFile, File, HTTPException
from models.salary import SalaryInput, SalaryOutput, BulkSalaryOutput, EmployeeData
from services.salary_service import SalaryService
import pandas as pd
from io import BytesIO
from typing import List

router = APIRouter(prefix="/api/salary", tags=["Salary"])

@router.post("/calculate", response_model=SalaryOutput)
async def calculate_salary(input_data: SalaryInput):
    """
    Calculate net salary from gross salary
    """
    result = SalaryService.handle_convert_gross_to_net(
        input_data.gross_salary, 
        input_data.number_of_dependents
    )
    return result

@router.post("/upload", response_model=BulkSalaryOutput)
async def upload_excel(file: UploadFile = File(...)):
    """
    Upload an Excel file and calculate net salary for all employees
    """
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")
    
    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))
        
        # Validate required columns
        required_columns = ["ID", "Employee Name", "Gross Salary", "Number of Dependents"]
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing required column: {col}")
        
        # Process each row
        results = []
        for _, row in df.iterrows():
            salary_result = SalaryService.handle_convert_gross_to_net(
                gross_salary=row["Gross Salary"],
                number_of_dependents=row["Number of Dependents"]
            )
            
            employee = EmployeeData(
                id=row["ID"],
                employee_name=row["Employee Name"],
                gross_salary=row["Gross Salary"],
                number_of_dependents=row["Number of Dependents"],
                net_salary=salary_result.net_salary
            )
            results.append(employee)
        
        return BulkSalaryOutput(result=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}") 