import pytest
from app.models.salary import SalaryOutput, TaxConfig, TaxBracket
from app.services.salary_service import SalaryService

class TestSalaryService:
    def test_get_tax_config(self):
        tax_config = SalaryService.get_tax_config()
        assert isinstance(tax_config, TaxConfig)
        assert len(tax_config.BRACKETS) == 7
        assert tax_config.BRACKETS[0].rate == 0.05
        assert tax_config.BRACKETS[0].limit == 5000000
        assert tax_config.BRACKETS[-1].rate == 0.35
    
    def test_calculate_insurance(self):
        gross_salary = 10000000
        expected_insurance = gross_salary * (0.08 + 0.015 + 0.01)  # Social + Health + Unemployment
        result = SalaryService.calculate_insurance(gross_salary)
        assert result == expected_insurance
        
    def test_calculate_personal_deduction(self):
        # Test with 0 dependents
        result = SalaryService.calculate_personal_deduction(0)
        assert result == 11000000
        
        # Test with 2 dependents
        result = SalaryService.calculate_personal_deduction(2)
        assert result == 11000000 + (2 * 4400000)
    
    def test_calculate_tax(self):
        tax_config = SalaryService.get_tax_config()
        
        # Test case 1: 0 income (no tax)
        assert SalaryService.calculate_tax(0, tax_config) == 0
        
        # Test case 2: Income in first bracket
        income = 4000000
        expected_tax = income * 0.05
        assert SalaryService.calculate_tax(income, tax_config) == expected_tax
        
        # Test case 3: Income spanning multiple brackets
        income = 15000000
        expected_tax = (5000000 * 0.05) + (5000000 * 0.1) + (5000000 * 0.15)
        assert SalaryService.calculate_tax(income, tax_config) == expected_tax

    def test_handle_convert_gross_to_net(self):
        # Test case 1: Basic calculation with no dependents
        gross_salary = 20000000
        dependents = 0
        
        result = SalaryService.handle_convert_gross_to_net(gross_salary, dependents)
        
        assert isinstance(result, SalaryOutput)
        assert result.gross_salary == gross_salary
        
        # Manual calculation to verify
        insurance = gross_salary * (0.08 + 0.015 + 0.01)
        taxable_income = gross_salary - insurance - 11000000
        
        # Calculate tax manually
        tax = 0
        brackets = [(0, 5000000, 0.05), (5000000, 10000000, 0.1), 
                   (10000000, 18000000, 0.15), (18000000, 32000000, 0.2),
                   (32000000, 52000000, 0.25), (52000000, 80000000, 0.3),
                   (80000000, float('inf'), 0.35)]
        
        previous_limit = 0
        for start, limit, rate in brackets:
            if taxable_income > previous_limit:
                bracket_taxable = min(taxable_income, limit) - previous_limit
                tax += bracket_taxable * rate
                previous_limit = limit
            else:
                break
        
        expected_net = gross_salary - insurance - tax
        
        assert round(result.insurance_amount, 2) == round(insurance, 2)
        assert round(result.personal_income_tax, 2) == round(tax, 2)
        assert round(result.net_salary, 2) == round(expected_net, 2)

        # Test case 2: With dependents
        dependents = 2
        result = SalaryService.handle_convert_gross_to_net(gross_salary, dependents)
        
        # Updated calculation with dependents
        taxable_income = gross_salary - insurance - (11000000 + 2 * 4400000)
        taxable_income = max(0, taxable_income)
        
        # Recalculate tax
        tax = 0
        previous_limit = 0
        for start, limit, rate in brackets:
            if taxable_income > previous_limit:
                bracket_taxable = min(taxable_income, limit) - previous_limit
                tax += bracket_taxable * rate
                previous_limit = limit
            else:
                break
        
        expected_net = gross_salary - insurance - tax
        
        assert round(result.personal_income_tax, 2) == round(tax, 2)
        assert round(result.net_salary, 2) == round(expected_net, 2)
        
