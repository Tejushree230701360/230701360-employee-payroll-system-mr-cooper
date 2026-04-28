
class Employee:
    def __init__(self, name, emp_id, gross_salary):
        self.name = name
        self.emp_id = emp_id
        self.gross_salary = gross_salary
        self.basic = 0
        self.hra = 0
        self.spl_allowance = 0
        self.pf = 0
        self.tds = 0
        self.deductions = 0
        self.net_salary = 0
        self.bank_account = None
        self.bank_name = None
    def calculate_salary(self):
        self.basic = self.gross_salary * 0.5  
        self.hra = self.basic * 0.4 
        self.spl_allowance = self.gross_salary - self.basic - self.hra
        self.pf = self.basic * 0.12
        self.tds = self.calculate_tds(self.gross_salary)
        self.deductions = self.pf + self.tds
        self.net_salary = self.gross_salary - self.deductions

    def calculate_tds(self, gross):
        if gross <= 250000:
            return 0
        elif gross <= 500000:
            return (gross - 250000) * 0.05
        elif gross <= 1000000:
            return 12500 + (gross - 500000) * 0.2
        else:
            return 112500 + (gross - 1000000) * 0.3

    def generate_payslip(self, month, year):
        payslip = f"""
        
                PAYSLIP FOR {month.upper()} {year}

        Employee Name: {self.name}
        Employee ID: {self.emp_id}

        EARNINGS:
        Basic Salary: ₹{self.basic:,.2f}
        HRA: ₹{self.hra:,.2f}
        Special Allowance: ₹{self.spl_allowance:,.2f}
        Gross Salary: ₹{self.gross_salary:,.2f}

        DEDUCTIONS:
        PF: ₹{self.pf:,.2f}
        TDS: ₹{self.tds:,.2f}
        Total Deductions: ₹{self.deductions:,.2f}

        NET SALARY: ₹{self.net_salary:,.2f}

       
        """
        return payslip

class HRManager:
    def __init__(self, name):
        self.name = name
    def select_payroll_period(self):
        month = input("Enter payroll month (e.g., January): ")
        year = input("Enter payroll year (e.g., 2024): ")
        print(f"Payroll period selected: {month} {year}")
        return month, year
    def calculate_net_salary(self, employee):
        employee.calculate_salary()
        print(f"Net salary calculated for {employee.name}: ₹{employee.net_salary:,.2f}")

class FinanceOfficer:
    def __init__(self, name):
        self.name = name
    def approve_salary(self, employee):
        print(f"Finance Manager {self.name} has approved the salary of ₹{employee.net_salary:,.2f} for {employee.name}.")
    def generate_payslip(self, employee, month, year):
        return employee.generate_payslip(month, year)
    def distribute_payslip(self, payslip):
        print("Distributing payslip to employee...")
        print(payslip)
    def transfer_salary(self, employee):
        if not hasattr(employee, 'bank_account') or not employee.bank_account:
            print("Error: Bank account details not found. Cannot transfer salary.")
            return False
        print(f"Transferring ₹{employee.net_salary:,.2f} to {employee.name}'s bank account ({employee.bank_name}, Account: {employee.bank_account}).")
        return True

employees = {
    "101": {"name": "valluru varshini", "gross": 500000, "bank_account": "1001234567890", "bank_name": "State Bank of India"},
    "102": {"name": "Varsha", "gross": 600000, "bank_account": "9876543210123", "bank_name": "HDFC Bank"},
    "103": {"name": "swetha J", "gross": 450000, "bank_account": "1234567890123", "bank_name": "ICICI Bank"},
    "104": {"name": "Tejushree sanjeevikumar", "gross": 300000, "bank_account": "3210987654321", "bank_name": "Axis Bank"},
    "105": {"name": "Uma AL", "gross": 700000},
}
processed_payrolls = set()
if __name__ == "__main__":
    hr_manager = HRManager("Alice")
    finance_officer = FinanceOfficer("Bob")
    
    while True:
        month, year = hr_manager.select_payroll_period()
    
        period_key = (month, year)
        if period_key in processed_payrolls:
            print(f"Warning: Payroll for {month} {year} has already been processed. Blocking duplicate processing.")
            another = input("Do you want to process payroll for another period? (yes/no): ").strip().lower()
            if another != 'yes':
                break
            continue
    
        print(f"\nProcessing payroll for all employees for {month} {year}...\n")
        
        processed_count = 0
        held_count = 0
    
        for emp_id, emp_data in employees.items():
            print(f"\n--- Processing Employee ID: {emp_id} ---")
            
            # Create employee object
            name = emp_data["name"]
            gross_salary = emp_data["gross"]
            employee = Employee(name, emp_id, gross_salary)
            employee.bank_account = emp_data.get("bank_account")
            employee.bank_name = emp_data.get("bank_name")
            
            if not employee.bank_account:
                print(f"Error: Bank account details not found for {name}. Holding this employee.")
                held_count += 1
                continue
            
            print(f"Employee: {name}, Gross Salary: ₹{gross_salary:,.2f}")
            print(f"Bank: {employee.bank_name}, Account: {employee.bank_account}")
            
            hr_manager.calculate_net_salary(employee)
            
            if employee.net_salary < 0:
                print(f"Alert: Net salary is negative (₹{employee.net_salary:,.2f}) due to excess deductions. Holding payroll for {name}.")
                held_count += 1
                continue
            
            # Process payroll
            finance_officer.approve_salary(employee)
            payslip = finance_officer.generate_payslip(employee, month, year)
            finance_officer.distribute_payslip(payslip)
            if finance_officer.transfer_salary(employee):
                processed_count += 1
                print(f"Payroll processed successfully for {name}.")
        if held_count == 0:
            processed_payrolls.add(period_key)
            print(f"\n\n========== PAYROLL SUMMARY FOR {month.upper()} {year} ==========")
            print(f"Total Employees Processed: {processed_count}")
            print(f"Total Employees Held: {held_count}")
            print(f"Payroll period {month} {year} has been locked for future processing.")
        else:
            print(f"\n\n========== PAYROLL SUMMARY FOR {month.upper()} {year} ==========")
            print(f"Total Employees Processed: {processed_count}")
            print(f"Total Employees Held: {held_count}")
            print(f"Payroll period {month} {year} has NOT been locked due to held employees.")
        
        another = input("Do you want to process payroll for another period? (yes/no): ").strip().lower()
        if another != 'yes':
            break



                
        


           

