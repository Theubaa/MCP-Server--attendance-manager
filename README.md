# Leave Management System

A comprehensive leave management system that stores all data locally in Excel files. This system provides a simple and efficient way to manage employee leave requests, approvals, and leave balance tracking without requiring any database setup.

## ✨ **Features**

- **👥 Employee Management**: Add, view, and manage employee information with leave entitlements
- **📝 Leave Application**: Submit leave requests with date ranges and reasons
- **✅ Leave Approval**: Approve or reject leave requests with comments
- **📊 Leave Balance Tracking**: Automatic tracking of used and remaining leaves
- **📅 Multiple Leave Types**: Annual, Sick, Personal, Maternity, Paternity leaves
- **🔄 Leave Cancellation**: Cancel approved leaves with automatic balance restoration
- **📈 Reporting**: Generate comprehensive leave reports and summaries
- **📤 Data Export**: Export data to separate Excel files for analysis
- **💾 Local Storage**: All data stored in organized Excel sheets (no database required)

## 📊 **Excel Sheet Structure**

### **Employees Sheet**
- Employee_ID
- Employee_Name
- Department
- Position
- Email
- Phone
- Join_Date
- Leave_Entitlement

### **Leave_Requests Sheet**
- Request_ID
- Employee_ID
- Employee_Name
- Leave_Type
- Start_Date
- End_Date
- Total_Days
- Reason
- Status
- Applied_Date
- Approved_By
- Approved_Date
- Comments

### **Leave_Balance Sheet**
- Employee_ID
- Employee_Name
- Leave_Type
- Total_Entitlement
- Used_Leaves
- Remaining_Leaves
- Year

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install pandas openpyxl
```

### **2. Use the System**
```python
from main import LeaveManagementSystem

# Initialize the system
leave_mgr = LeaveManagementSystem("my_leave_system.xlsx")

# Add an employee
leave_mgr.add_employee(
    employee_id="EMP001",
    name="vibhanshu",
    department="IT",
    position="Developer",
    email="vibhanshu@gaincafe.com",
    phone="123-456-7890",
    leave_entitlement=25
)

# Apply for leave
leave_mgr.apply_leave("EMP001", "Annual Leave", "2025-02-15", "2025-02-20", "Family vacation")

# Approve leave
leave_mgr.approve_leave("LR2025020112000000", "HR Manager", "Approved", "Approved as requested")

# Check leave balance
balance = leave_mgr.get_leave_balance("EMP001")
print(balance)
```

## 📋 **Available Methods**

### **Employee Management**
- `add_employee(employee_id, name, department, position, email, phone, join_date, leave_entitlement)`: Add new employee
- `get_employee_list()`: Get list of all employees
- `get_employee_name(employee_id)`: Get employee name by ID

### **Leave Management**
- `apply_leave(employee_id, leave_type, start_date, end_date, reason)`: Submit leave request
- `approve_leave(request_id, approved_by, status, comments)`: Approve/reject leave
- `cancel_leave(request_id, employee_id)`: Cancel leave request
- `get_leave_requests(employee_id, status)`: Get leave requests with filtering

### **Leave Balance & Reporting**
- `get_leave_balance(employee_id)`: Get leave balance for employees
- `get_leave_summary(year)`: Get annual leave summary
- `export_to_excel(filename)`: Export data to Excel file

## 📅 **Leave Types & Entitlements**

The system automatically sets up different leave types with standard entitlements:

- **Annual Leave**: Based on employee's leave entitlement (default: 25 days)
- **Sick Leave**: 15 days per year
- **Personal Leave**: 5 days per year
- **Maternity Leave**: 90 days per year
- **Paternity Leave**: 15 days per year

## 🔄 **Workflow**

### **1. Employee Setup**
```python
# Add employee with leave entitlement
leave_mgr.add_employee("EMP001", "vibhanshu", "IT", "Developer", 
                      "vibhanshu@gaincafe.com", "123-456-7890", leave_entitlement=25)
```

### **2. Leave Application**
```python
# Employee applies for leave
leave_mgr.apply_leave("EMP001", "Annual Leave", "2025-02-15", "2025-02-20", "Family vacation")
```

### **3. Leave Approval**
```python
# Manager approves/rejects leave
leave_mgr.approve_leave("LR2025020112000000", "HR Manager", "Approved", "Approved as requested")
```

### **4. Leave Cancellation**
```python
# Employee cancels approved leave
leave_mgr.cancel_leave("LR2025020112000000", "EMP001")
```

## 📊 **Usage Examples**

### **Daily Leave Management**
```python
# Get all pending leave requests
pending_leaves = leave_mgr.get_leave_requests(status="Pending")
print(f"Pending requests: {len(pending_leaves)}")

# Get leave balance for specific employee
balance = leave_mgr.get_leave_balance("EMP001")
print(balance)

# Get annual summary
summary = leave_mgr.get_leave_summary(2025)
print(f"Approval rate: {summary['approval_rate']}%")
```

### **Batch Operations**
```python
# Add multiple employees
employees = [
    ("EMP002", "gaurav", "HR", "Manager", "gaurav@gaincafe.com", "123-456-7891", 25),
    ("EMP003", "lakshay", "SEO", "Specialist", "seo@gaincafe.com", "123-456-7892", 25),
    ("EMP004", "manasvi", "Marketing", "Coordinator", "manasvi@gaincafe.com", "123-456-7893", 25)
]

for emp in employees:
    leave_mgr.add_employee(*emp)
```

### **Generate Reports**
```python
# Export all data to Excel
leave_mgr.export_to_excel("monthly_leave_report.xlsx")

# Get leave requests for specific employee
employee_leaves = leave_mgr.get_leave_requests(employee_id="EMP001")
print(employee_leaves)
```

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Code     │───▶│ Leave Management │───▶│  Local Excel    │
│                 │    │ System           │    │ Files           │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 **File Structure**

```
my-first-mcp-server/
├── main.py                    # Leave management system
├── pyproject.toml            # Project dependencies
├── README.md                 # This documentation
├── leave_management.xlsx     # Main data file (generated after first run)
└── leave_management_report.xlsx # Exported reports (generated on demand)
```

## 🔧 **Configuration**

### **Default Settings**
- **Working Days**: Monday to Friday (weekends excluded from leave calculations)
- **Leave Entitlement**: 25 days annual leave (configurable per employee)
- **Date Format**: YYYY-MM-DD
- **Request ID Format**: LR + timestamp

### **Customization**
You can easily modify:
- Leave entitlements per employee
- Working day calculations
- Leave types and their entitlements
- Request ID format
- Excel file structure

## 🚨 **Error Handling**

The system includes comprehensive error handling for:
- **Invalid dates** (past dates, end before start)
- **Insufficient leave balance**
- **Missing employees**
- **Invalid leave types**
- **File operations**
- **Data validation**

## 📈 **Performance Features**

- **Efficient Excel operations** with openpyxl
- **Smart data filtering** and searching
- **Batch operations** for multiple updates
- **Automatic calculations** (working days, leave balance)
- **Data integrity checks** before operations

## 🆘 **Troubleshooting**

### **Common Issues**

1. **"Insufficient leave balance" error**
   - Check current leave balance
   - Verify leave type and year
   - Ensure leave entitlements are set correctly

2. **"Employee not found" error**
   - Verify employee ID spelling
   - Check if employee exists in the system
   - Ensure proper employee setup

3. **"Invalid date" error**
   - Use YYYY-MM-DD format
   - Ensure dates are not in the past
   - Check start date is before end date

### **Getting Help**

If you encounter issues:
1. Check the error message for specific details
2. Verify Excel file permissions
3. Ensure proper data format
4. Check file path and accessibility

## 📚 **API Reference**

For detailed API documentation, see the inline docstrings in the `main.py` file. Each method includes:
- Parameter descriptions
- Return value information
- Usage examples
- Error handling details

## 🎉 **Ready to Use!**

Your leave management system is now ready! The system will automatically:

- ✅ Create organized Excel files
- ✅ Set up employee leave entitlements
- ✅ Track leave balances automatically
- ✅ Calculate working days (excluding weekends)
- ✅ Generate unique request IDs
- ✅ Maintain data integrity
- ✅ Provide comprehensive reporting

Start managing employee leaves efficiently with just a few lines of Python code!

## 🚀 **Running the System**

To run the demonstration:

```bash
python main.py
```

This will:
1. Initialize the leave management system
2. Add sample employees (vibhanshu, gaurav, lakshay, manasvi, kanchi)
3. Simulate leave requests
4. Demonstrate approval workflow
5. Show leave balance tracking
6. Export sample data to Excel

## 📊 **Sample Data Included**

The system comes with sample data for your existing employees:
- **vibhanshu** - IT Developer
- **gaurav** - HR Manager  
- **lakshay** - SEO Specialist
- **manasvi** - Marketing Coordinator
- **kanchi** - HR Assistant

All employees start with 25 days annual leave entitlement and full leave balances for the current year.
