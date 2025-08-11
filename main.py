from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

class LeaveManagementSystem:
    def __init__(self):
        """Initialize the leave management system with in-memory data"""
        self.employees = {}
        self.leave_requests = {}
        self.leave_balance = {}
        self.request_counter = 1
        self.initialize_mock_data()
    
    def initialize_mock_data(self):
        """Initialize the system with mock data"""
        print("Initializing Leave Management System with mock data...")
        
        # Add sample employees
        self.add_employee("EMP001", "vibhanshu", "IT", "Developer", "vibhanshu@gaincafe.com", "123-456-7890", leave_entitlement=25)
        self.add_employee("EMP002", "gaurav", "HR", "Manager", "gaurav@gaincafe.com", "123-456-7891", leave_entitlement=25)
        self.add_employee("EMP003", "lakshay", "SEO", "Specialist", "seo@gaincafe.com", "123-456-7892", leave_entitlement=25)
        self.add_employee("EMP004", "manasvi", "Marketing", "Coordinator", "manasvi@gaincafe.com", "123-456-7893", leave_entitlement=25)
        self.add_employee("EMP005", "kanchi", "HR", "Assistant", "hr@gaincafe.com", "123-456-7894", leave_entitlement=25)
        
        # Add some sample leave requests
        self.apply_leave("EMP001", "Annual Leave", "2025-02-15", "2025-02-20", "Family vacation")
        self.apply_leave("EMP002", "Sick Leave", "2025-02-10", "2025-02-12", "Not feeling well")
        self.apply_leave("EMP003", "Personal Leave", "2025-02-25", "2025-02-25", "Personal appointment")
        
        # Approve some leaves
        self.approve_leave("LR001", "HR Manager", "Approved", "Approved as requested")
        self.approve_leave("LR002", "HR Manager", "Approved", "Approved")
        
        print("Mock data initialized successfully!")
    
    def add_employee(self, employee_id: str, name: str, department: str, position: str, 
                    email: str, phone: str, join_date: str = None, leave_entitlement: int = 25) -> bool:
        """Add a new employee to the system"""
        try:
            if join_date is None:
                join_date = date.today().strftime("%Y-%m-%d")
            
            # Check if employee already exists
            if employee_id in self.employees:
                print(f"Employee with ID {employee_id} already exists!")
                return False
            
            # Add new employee
            self.employees[employee_id] = {
                'id': employee_id,
                'name': name,
                'department': department,
                'position': position,
                'email': email,
                'phone': phone,
                'join_date': join_date,
                'leave_entitlement': leave_entitlement
            }
            
            # Initialize leave balance for the employee
            current_year = date.today().year
            self.initialize_leave_balance(employee_id, name, leave_entitlement, current_year)
            
            print(f"Employee {name} added successfully with {leave_entitlement} days leave entitlement!")
            return True
            
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False
    
    def initialize_leave_balance(self, employee_id: str, employee_name: str, entitlement: int, year: int):
        """Initialize leave balance for different leave types"""
        leave_types = ["Annual Leave", "Sick Leave", "Personal Leave", "Maternity Leave", "Paternity Leave"]
        
        if employee_id not in self.leave_balance:
            self.leave_balance[employee_id] = {}
        
        for leave_type in leave_types:
            # Set different entitlements for different leave types
            if leave_type == "Annual Leave":
                total_entitlement = entitlement
            elif leave_type == "Sick Leave":
                total_entitlement = 15
            elif leave_type == "Personal Leave":
                total_entitlement = 5
            elif leave_type == "Maternity Leave":
                total_entitlement = 90
            elif leave_type == "Paternity Leave":
                total_entitlement = 15
            
            self.leave_balance[employee_id][leave_type] = {
                'employee_id': employee_id,
                'employee_name': employee_name,
                'leave_type': leave_type,
                'total_entitlement': total_entitlement,
                'used_leaves': 0,
                'remaining_leaves': total_entitlement,
                'year': year
            }
    
    def apply_leave(self, employee_id: str, leave_type: str, start_date: str, end_date: str, 
                   reason: str = "") -> bool:
        """Apply for leave"""
        try:
            # Normalize leave type (case-insensitive)
            leave_type = leave_type.strip().title()
            
            # Validate leave type
            valid_leave_types = ["Annual Leave", "Sick Leave", "Personal Leave", "Maternity Leave", "Paternity Leave"]
            if leave_type not in valid_leave_types:
                print(f"Invalid leave type! Please choose from: {', '.join(valid_leave_types)}")
                return False
            
            # Try multiple date formats
            start_dt = None
            end_dt = None
            
            date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]
            
            for fmt in date_formats:
                try:
                    start_dt = datetime.strptime(start_date, fmt).date()
                    break
                except ValueError:
                    continue
            
            for fmt in date_formats:
                try:
                    end_dt = datetime.strptime(end_date, fmt).date()
                    break
                except ValueError:
                    continue
            
            if start_dt is None or end_dt is None:
                print("Invalid date format! Please use YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY")
                return False
            
            if start_dt > end_dt:
                print("Start date cannot be after end date!")
                return False
            
            if start_dt < date.today():
                print("Cannot apply for leave in the past!")
                return False
            
            # Calculate total days (excluding weekends)
            total_days = self.calculate_working_days(start_dt, end_dt)
            
            # Check leave balance
            if not self.check_leave_balance(employee_id, leave_type, total_days):
                return False
            
            # Get employee name
            employee_name = self.get_employee_name(employee_id)
            if not employee_name:
                print(f"Employee with ID {employee_id} not found!")
                return False
            
            # Generate request ID
            request_id = f"LR{self.request_counter:03d}"
            self.request_counter += 1
            
            # Add leave request
            self.leave_requests[request_id] = {
                'request_id': request_id,
                'employee_id': employee_id,
                'employee_name': employee_name,
                'leave_type': leave_type,
                'start_date': start_dt.strftime("%Y-%m-%d"),
                'end_date': end_dt.strftime("%Y-%m-%d"),
                'total_days': total_days,
                'reason': reason,
                'status': 'Pending',
                'applied_date': datetime.now().strftime("%Y-%m-%d"),
                'approved_by': None,
                'approved_date': None,
                'comments': None
            }
            
            print(f"Leave request submitted successfully! Request ID: {request_id}")
            print(f"Leave Type: {leave_type}, Duration: {total_days} days")
            return True
            
        except Exception as e:
            print(f"Error applying for leave: {e}")
            return False
    
    def calculate_working_days(self, start_date: date, end_date: date) -> int:
        """Calculate working days excluding weekends"""
        working_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday to Friday (0-4)
                working_days += 1
            current_date += timedelta(days=1)
        
        return working_days
    
    def check_leave_balance(self, employee_id: str, leave_type: str, requested_days: int) -> bool:
        """Check if employee has sufficient leave balance"""
        try:
            if employee_id in self.leave_balance and leave_type in self.leave_balance[employee_id]:
                remaining_leaves = self.leave_balance[employee_id][leave_type]['remaining_leaves']
                if remaining_leaves >= requested_days:
                    return True
                else:
                    print(f"Insufficient leave balance! Available: {remaining_leaves} days, Requested: {requested_days} days")
                    return False
            else:
                print(f"No leave balance found for {leave_type}")
                return False
                
        except Exception as e:
            print(f"Error checking leave balance: {e}")
            return False
    
    def get_employee_name(self, employee_id: str) -> Optional[str]:
        """Get employee name by ID"""
        if employee_id in self.employees:
            return self.employees[employee_id]['name']
        return None
    
    def approve_leave(self, request_id: str, approved_by: str, status: str = "Approved", comments: str = "") -> bool:
        """Approve or reject leave request"""
        try:
            if request_id not in self.leave_requests:
                print(f"Leave request {request_id} not found!")
                return False
            
            # Update status
            self.leave_requests[request_id]['status'] = status
            self.leave_requests[request_id]['approved_by'] = approved_by
            self.leave_requests[request_id]['approved_date'] = datetime.now().strftime("%Y-%m-%d")
            self.leave_requests[request_id]['comments'] = comments
            
            # If approved, update leave balance
            if status == "Approved":
                employee_id = self.leave_requests[request_id]['employee_id']
                leave_type = self.leave_requests[request_id]['leave_type']
                total_days = self.leave_requests[request_id]['total_days']
                self.update_leave_balance(employee_id, leave_type, total_days)
            
            print(f"Leave request {request_id} {status.lower()}")
            return True
            
        except Exception as e:
            print(f"Error approving leave: {e}")
            return False
    
    def update_leave_balance(self, employee_id: str, leave_type: str, used_days: int):
        """Update leave balance after leave approval"""
        try:
            if employee_id in self.leave_balance and leave_type in self.leave_balance[employee_id]:
                current_used = self.leave_balance[employee_id][leave_type]['used_leaves']
                current_remaining = self.leave_balance[employee_id][leave_type]['remaining_leaves']
                
                new_used = current_used + used_days
                new_remaining = current_remaining - used_days
                
                self.leave_balance[employee_id][leave_type]['used_leaves'] = new_used
                self.leave_balance[employee_id][leave_type]['remaining_leaves'] = new_remaining
                
                print(f"Updated leave balance for {leave_type}: Used {new_used}, Remaining {new_remaining}")
                
        except Exception as e:
            print(f"Error updating leave balance: {e}")
    
    def get_leave_requests(self, employee_id: str = None, status: str = None) -> List[Dict]:
        """Get leave requests with optional filtering"""
        try:
            requests = list(self.leave_requests.values())
            
            # Apply filters
            if employee_id:
                requests = [req for req in requests if req['employee_id'] == employee_id]
            
            if status:
                requests = [req for req in requests if req['status'] == status]
            
            return requests
            
        except Exception as e:
            print(f"Error getting leave requests: {e}")
            return []
    
    def get_leave_balance(self, employee_id: str = None) -> List[Dict]:
        """Get leave balance for employees"""
        try:
            if employee_id:
                if employee_id in self.leave_balance:
                    return list(self.leave_balance[employee_id].values())
                else:
                    return []
            else:
                # Return all balances
                all_balances = []
                for emp_balances in self.leave_balance.values():
                    all_balances.extend(emp_balances.values())
                return all_balances
                
        except Exception as e:
            print(f"Error getting leave balance: {e}")
            return []
    
    def get_employee_list(self) -> List[Dict]:
        """Get list of all employees"""
        try:
            return list(self.employees.values())
        except Exception as e:
            print(f"Error getting employee list: {e}")
            return []
    
    def cancel_leave(self, request_id: str, employee_id: str) -> bool:
        """Cancel a leave request"""
        try:
            if request_id not in self.leave_requests:
                print(f"Leave request {request_id} not found!")
                return False
            
            request = self.leave_requests[request_id]
            if request['employee_id'] != employee_id:
                print(f"Leave request {request_id} not authorized for this employee!")
                return False
            
            current_status = request['status']
            
            if current_status == "Approved":
                # If already approved, restore leave balance
                leave_type = request['leave_type']
                total_days = request['total_days']
                self.restore_leave_balance(employee_id, leave_type, total_days)
            
            # Update status to cancelled
            request['status'] = "Cancelled"
            request['comments'] = "Cancelled by employee"
            
            print(f"Leave request {request_id} cancelled successfully")
            return True
            
        except Exception as e:
            print(f"Error cancelling leave: {e}")
            return False
    
    def restore_leave_balance(self, employee_id: str, leave_type: str, days: int):
        """Restore leave balance when leave is cancelled"""
        try:
            if employee_id in self.leave_balance and leave_type in self.leave_balance[employee_id]:
                current_used = self.leave_balance[employee_id][leave_type]['used_leaves']
                current_remaining = self.leave_balance[employee_id][leave_type]['remaining_leaves']
                
                new_used = current_used - days
                new_remaining = current_remaining + days
                
                self.leave_balance[employee_id][leave_type]['used_leaves'] = new_used
                self.leave_balance[employee_id][leave_type]['remaining_leaves'] = new_remaining
                
                print(f"Restored leave balance for {leave_type}: Used {new_used}, Remaining {new_remaining}")
                
        except Exception as e:
            print(f"Error restoring leave balance: {e}")
    
    def get_leave_summary(self, year: int = None) -> Dict:
        """Get leave summary for the year"""
        try:
            if year is None:
                year = date.today().year
            
            leave_requests = list(self.leave_requests.values())
            
            # Filter by year
            year_requests = []
            for request in leave_requests:
                request_year = datetime.strptime(request['start_date'], "%Y-%m-%d").year
                if request_year == year:
                    year_requests.append(request)
            
            if not year_requests:
                return {}
            
            # Calculate summary
            total_requests = len(year_requests)
            approved_requests = len([req for req in year_requests if req['status'] == 'Approved'])
            pending_requests = len([req for req in year_requests if req['status'] == 'Pending'])
            rejected_requests = len([req for req in year_requests if req['status'] == 'Rejected'])
            
            # Total days
            total_days = sum(req['total_days'] for req in year_requests)
            approved_days = sum(req['total_days'] for req in year_requests if req['status'] == 'Approved')
            
            return {
                'year': year,
                'total_requests': total_requests,
                'approved_requests': approved_requests,
                'pending_requests': pending_requests,
                'rejected_requests': rejected_requests,
                'total_days_requested': total_days,
                'total_days_approved': approved_days,
                'approval_rate': round((approved_requests / total_requests) * 100, 2) if total_requests > 0 else 0
            }
            
        except Exception as e:
            print(f"Error getting leave summary: {e}")
            return {}
    
    def display_current_status(self):
        """Display current system status"""
        print("\n" + "="*60)
        print("📊 LEAVE MANAGEMENT SYSTEM - CURRENT STATUS")
        print("="*60)
        
        # Display employees
        print(f"\n👥 EMPLOYEES ({len(self.employees)}):")
        for emp_id, emp in self.employees.items():
            print(f"  • {emp['name']} ({emp_id}) - {emp['department']} - {emp['position']}")
            print(f"    Email: {emp['email']} | Leave Entitlement: {emp['leave_entitlement']} days")
        
        # Display leave requests
        print(f"\n📝 LEAVE REQUESTS ({len(self.leave_requests)}):")
        for req_id, req in self.leave_requests.items():
            status_icon = "✅" if req['status'] == 'Approved' else "⏳" if req['status'] == 'Pending' else "❌"
            print(f"  {status_icon} {req_id}: {req['employee_name']} - {req['leave_type']}")
            print(f"    {req['start_date']} to {req['end_date']} ({req['total_days']} days) - {req['status']}")
            if req['reason']:
                print(f"    Reason: {req['reason']}")
        
        # Display leave balance
        print(f"\n💰 LEAVE BALANCE:")
        for emp_id, balances in self.leave_balance.items():
            emp_name = self.employees[emp_id]['name']
            print(f"  📋 {emp_name}:")
            for leave_type, balance in balances.items():
                print(f"    • {leave_type}: {balance['remaining_leaves']}/{balance['total_entitlement']} days remaining")
        
        print("\n" + "="*60)

    def display_available_employees(self):
        """Display available employees for user selection"""
        print("\n📋 Available Employees:")
        for emp_id, emp in self.employees.items():
            print(f"  {emp_id}: {emp['name']} - {emp['department']} - {emp['position']}")
    
    def get_employee_id_from_input(self, user_input: str) -> str:
        """Convert user input to proper employee ID format"""
        user_input = user_input.strip()
        
        # If user enters just a number, convert to EMP format
        if user_input.isdigit():
            emp_num = int(user_input)
            if 1 <= emp_num <= 99:
                return f"EMP{emp_num:03d}"
        
        # If user enters EMP format, validate it exists
        if user_input in self.employees:
            return user_input
        
        # If user enters name, try to find by name
        for emp_id, emp in self.employees.items():
            if emp['name'].lower() == user_input.lower():
                return emp_id
        
        return user_input  # Return as-is if no conversion possible

def main():
    """Main function to demonstrate the leave management system"""
    print("=== Leave Management System (Mock Data) ===")
    print("Initializing system with mock data...")
    
    # Initialize leave management system
    leave_mgr = LeaveManagementSystem()
    
    # Display current status
    leave_mgr.display_current_status()
    
    # Interactive menu
    while True:
        print("\n" + "="*50)
        print("🎯 LEAVE MANAGEMENT SYSTEM - MAIN MENU")
        print("="*50)
        print("1. View Current Status")
        print("2. Add New Employee")
        print("3. Apply for Leave")
        print("4. Approve/Reject Leave")
        print("5. Cancel Leave")
        print("6. View Leave Requests")
        print("7. View Leave Balance")
        print("8. View Annual Summary")
        print("9. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            leave_mgr.display_current_status()
            
        elif choice == "2":
            print("\n--- Add New Employee ---")
            emp_id = input("Employee ID: ").strip()
            name = input("Name: ").strip()
            dept = input("Department: ").strip()
            position = input("Position: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            entitlement = input("Leave Entitlement (default 25): ").strip()
            entitlement = int(entitlement) if entitlement.isdigit() else 25
            
            leave_mgr.add_employee(emp_id, name, dept, position, email, phone, leave_entitlement=entitlement)
            
        elif choice == "3":
            print("\n--- Apply for Leave ---")
            leave_mgr.display_available_employees()
            emp_input = input("Employee ID, Name, or Number (e.g., 1, EMP001, vibhanshu): ").strip()
            emp_id = leave_mgr.get_employee_id_from_input(emp_input)
            
            print(f"\nAvailable Leave Types: Annual Leave, Sick Leave, Personal Leave, Maternity Leave, Paternity Leave")
            leave_type = input("Leave Type: ").strip()
            start_date = input("Start Date (YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY): ").strip()
            end_date = input("End Date (YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY): ").strip()
            reason = input("Reason: ").strip()
            
            leave_mgr.apply_leave(emp_id, leave_type, start_date, end_date, reason)
            
        elif choice == "4":
            print("\n--- Approve/Reject Leave ---")
            if not leave_mgr.leave_requests:
                print("No leave requests found!")
                continue
                
            print("\nAvailable Leave Requests:")
            for req_id, req in leave_mgr.leave_requests.items():
                if req['status'] == 'Pending':
                    print(f"  {req_id}: {req['employee_name']} - {req['leave_type']} ({req['start_date']} to {req['end_date']})")
            
            req_id = input("Request ID: ").strip()
            approver = input("Approver Name: ").strip()
            status = input("Status (Approved/Rejected): ").strip()
            comments = input("Comments: ").strip()
            
            leave_mgr.approve_leave(req_id, approver, status, comments)
            
        elif choice == "5":
            print("\n--- Cancel Leave ---")
            if not leave_mgr.leave_requests:
                print("No leave requests found!")
                continue
                
            print("\nAvailable Leave Requests:")
            for req_id, req in leave_mgr.leave_requests.items():
                print(f"  {req_id}: {req['employee_name']} - {req['leave_type']} ({req['status']})")
            
            req_id = input("Request ID: ").strip()
            emp_input = input("Employee ID, Name, or Number: ").strip()
            emp_id = leave_mgr.get_employee_id_from_input(emp_input)
            
            leave_mgr.cancel_leave(req_id, emp_id)
            
        elif choice == "6":
            print("\n--- Leave Requests ---")
            leave_mgr.display_available_employees()
            emp_input = input("Employee ID, Name, or Number (press Enter for all): ").strip()
            emp_id = leave_mgr.get_employee_id_from_input(emp_input) if emp_input else None
            
            print("\nAvailable Statuses: Pending, Approved, Rejected, Cancelled")
            status = input("Status (press Enter for all): ").strip()
            
            requests = leave_mgr.get_leave_requests(
                employee_id=emp_id if emp_id else None,
                status=status if status else None
            )
            
            if requests:
                for req in requests:
                    print(f"\nRequest ID: {req['request_id']}")
                    print(f"Employee: {req['employee_name']} ({req['employee_id']})")
                    print(f"Leave Type: {req['leave_type']}")
                    print(f"Dates: {req['start_date']} to {req['end_date']} ({req['total_days']} days)")
                    print(f"Status: {req['status']}")
                    print(f"Reason: {req['reason']}")
            else:
                print("No leave requests found.")
                
        elif choice == "7":
            print("\n--- Leave Balance ---")
            leave_mgr.display_available_employees()
            emp_input = input("Employee ID, Name, or Number (press Enter for all): ").strip()
            emp_id = leave_mgr.get_employee_id_from_input(emp_input) if emp_input else None
            
            balances = leave_mgr.get_leave_balance(emp_id if emp_id else None)
            
            if balances:
                for balance in balances:
                    print(f"\n{balance['employee_name']} - {balance['leave_type']}")
                    print(f"  Total: {balance['total_entitlement']} days")
                    print(f"  Used: {balance['used_leaves']} days")
                    print(f"  Remaining: {balance['remaining_leaves']} days")
            else:
                print("No leave balance found.")
                
        elif choice == "8":
            print("\n--- Annual Summary ---")
            year = input("Year (press Enter for current year): ").strip()
            year = int(year) if year.isdigit() else date.today().year
            
            summary = leave_mgr.get_leave_summary(year)
            
            if summary:
                print(f"\nLeave Summary for {summary['year']}:")
                print(f"  Total Requests: {summary['total_requests']}")
                print(f"  Approved: {summary['approved_requests']}")
                print(f"  Pending: {summary['pending_requests']}")
                print(f"  Rejected: {summary['rejected_requests']}")
                print(f"  Total Days Requested: {summary['total_days_requested']}")
                print(f"  Total Days Approved: {summary['total_days_approved']}")
                print(f"  Approval Rate: {summary['approval_rate']}%")
            else:
                print(f"No data found for year {year}.")
                
        elif choice == "9":
            print("\nThank you for using the Leave Management System!")
            break
            
        else:
            print("Invalid choice! Please enter a number between 1-9.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
