from app.models.salary import SalaryOutput, TaxConfig, TaxBracket

class SalaryService:
    # Constants regulation
    SOCIAL_INSURANCE_RATE = 0.08
    HEALTH_INSURANCE_RATE = 0.015
    UNEMPLOYMENT_INSURANCE_RATE = 0.01

    PERSONAL_DEDUCTION = 11000000 # 11 triệu đồng
    DEPENDENT_DEDUCTION = 4400000 # 4,4 triệu đồng

    TAX_BRACKET = [
        (0, 5000000, 0.05),
        (5000000, 10000000, 0.1),
        (10000000, 18000000, 0.15),
        (18000000, 32000000, 0.2),
        (32000000, 52000000, 0.25),
        (52000000, 80000000, 0.3),
        (80000000, float('inf'), 0.35)
    ]

    @classmethod
    def get_tax_config(cls):
        """Convert TAX_BRACKET to TaxConfig structure"""
        brackets = []
        for _, limit, rate in cls.TAX_BRACKET:
            brackets.append(TaxBracket(limit=limit, rate=rate))
        return TaxConfig(BRACKETS=brackets)

    @classmethod
    def calculate_insurance(cls, gross_salary):
        social_insurance = gross_salary * cls.SOCIAL_INSURANCE_RATE
        health_insurance = gross_salary * cls.HEALTH_INSURANCE_RATE
        unemployment_insurance = gross_salary * cls.UNEMPLOYMENT_INSURANCE_RATE
        return social_insurance + health_insurance + unemployment_insurance
    
    @classmethod
    def calculate_personal_deduction(cls, number_of_dependents):
        return cls.PERSONAL_DEDUCTION + number_of_dependents * cls.DEPENDENT_DEDUCTION
    
    @classmethod
    def calculate_tax(cls, pre_tax_income: float, tax_config: TaxConfig) -> float:
        tax = 0
        previous_limit = 0
        for bracket in tax_config.BRACKETS:
            limit, rate = bracket.limit, bracket.rate
            if pre_tax_income > previous_limit:
                taxable_income = min(pre_tax_income, limit) - previous_limit
                tax += taxable_income * rate
                previous_limit = limit
            else:
                break

        return tax

    @classmethod
    def handle_convert_gross_to_net(
        cls, gross_salary: float, number_of_dependents: int
    ) -> SalaryOutput:
        """Convert gross salary to net salary.

        Apply:
        - personal and dependent deductions
        - insurance contributions
        - personal income tax
        """
        # Get tax configuration
        tax_config_dep = cls.get_tax_config()
        
        # Step 1: Calculate insurance once
        insurance_amount = cls.calculate_insurance(gross_salary)

        # Step 2: Compute taxable income (pre-tax income)
        pre_tax_income = (
            gross_salary
            - insurance_amount
            - cls.calculate_personal_deduction(number_of_dependents)
        )
        
        pre_tax_income = max(0, pre_tax_income)

        # Step 3: Calculate personal income tax
        personal_income_tax = cls.calculate_tax(pre_tax_income, tax_config_dep)

        # Step 4: Compute net salary
        net_salary = gross_salary - insurance_amount - personal_income_tax

        return SalaryOutput(
            gross_salary=gross_salary,
            net_salary=net_salary,
            insurance_amount=insurance_amount,
            personal_income_tax=personal_income_tax,
        )
        