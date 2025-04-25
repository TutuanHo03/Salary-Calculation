import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.salary import SalaryInput, EmployeeData
from app.services.salary_service import SalaryService
import pandas as pd
from io import BytesIO
import os

client = TestClient(app)

class TestSalaryRoutes:

    def test_calculate_salary_endpoint(self):
        # Test case 1: Basic calculation with no dependents
        test_data = {
            "gross_salary": 20000000,
            "number_of_dependents": 1
        }
        expected_result = SalaryService.handle_convert_gross_to_net(test_data["gross_salary"], test_data["number_of_dependents"])

        response = client.post("/api/salary/calculate", json=test_data)
        assert response.status_code == 200
        result = response.json()
        assert result["gross_salary"] == test_data["gross_salary"]
        assert round(result["net_salary"], 2) == round(expected_result.net_salary, 2)
        assert round(result["insurance_amount"], 2) == round(expected_result.insurance_amount, 2)
        assert round(result["personal_income_tax"], 2) == round(expected_result.personal_income_tax, 2)
        
    def test_upload_excel_endpoint(self, tmp_path):
        test_data = {
            "ID": [1, 2, 3],
            "Employee Name": ["John Doe", "Jane Smith", "Mike Johnson"],
            "Gross Salary": [20000000, 30000000, 15000000],
            "Number of Dependents": [0, 2, 1]
        }

        df = pd.DataFrame(test_data)
        excel_file = tmp_path / "data_test_gross_net.xlsx"
        df.to_excel(excel_file, index=False)

        # Open file for reading
        with open(excel_file, "rb") as f:
            # Test API endpoint
            response = client.post(
                "/api/salary/upload",
                files={"file": ("data_test_gross_net.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        # Assertions
        assert response.status_code == 200
        result = response.json()
        
        assert "result" in result
        assert len(result["result"]) == 3
        
        # Check first employee result
        employee1 = result["result"][0]
        assert employee1["id"] == 1
        assert employee1["employee_name"] == "John Doe"
        assert employee1["gross_salary"] == 20000000
        assert employee1["number_of_dependents"] == 0
        
        # Calculate expected net salary for verification
        expected_net = SalaryService.handle_convert_gross_to_net(
            20000000, 0
        ).net_salary
        
        assert round(employee1["net_salary"], 2) == round(expected_net, 2)
    
    def test_upload_excel_invalid_format(self):
        # Create text file instead of Excel
        content = b"This is not an Excel file"
        
        # Test API endpoint with invalid file
        response = client.post(
            "/api/salary/upload",
            files={"file": ("test.txt", content, "text/plain")}
        )
        
        # Assertions
        assert response.status_code == 400
        assert "Invalid file format" in response.json()["detail"]
    
    def test_upload_excel_missing_columns(self, tmp_path):
        # Create test Excel file with missing columns
        test_data = {
            "ID": [1, 2, 3],
            "Employee Name": ["John Doe", "Jane Smith", "Mike Johnson"],
            # Missing "Gross Salary" and "Number of Dependents"
        }
        
        df = pd.DataFrame(test_data)
        excel_file = tmp_path / "invalid_employees.xlsx"
        df.to_excel(excel_file, index=False)
        
        # Open file for reading
        with open(excel_file, "rb") as f:
            # Test API endpoint
            response = client.post(
                "/api/salary/upload",
                files={"file": ("invalid_employees.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )
        
        # Assertions
        assert response.status_code == 400
        assert "Missing required column" in response.json()["detail"]

