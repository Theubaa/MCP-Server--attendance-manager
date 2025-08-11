#!/usr/bin/env python3
"""
Leave Management System MCP Server
For use with Claude Desktop using FastMCP
"""

from fastmcp import FastMCP
from main import LeaveManagementSystem
from typing import Optional

# Create the FastMCP server instance that Claude Desktop expects
mcp = FastMCP("leave-management")

# Initialize the leave management system
leave_mgr = LeaveManagementSystem()

@mcp.tool()
def view_employees() -> str:
    """View all employees in the system"""
    employees = leave_mgr.get_employee_list()
    if not employees:
        return "No employees found in the system."
    
    result = "👥 **EMPLOYEES**\n\n"
    for emp in employees:
        result += f"**{emp['name']}** ({emp['id']})\n"
        result += f"  Department: {emp['department']}\n"
        result += f"  Position: {emp['position']}\n"
        result += f"  Email: {emp['email']}\n"
        result += f"  Leave Entitlement: {emp['leave_entitlement']} days\n\n"
    return result

@mcp.tool()
def add_employee(
    employee_id: str,
    name: str,
    department: str,
    position: str,
    email: str,
    phone: str,
    leave_entitlement: int = 25
) -> str:
    """Add a new employee to the system"""
    success = leave_mgr.add_employee(
        employee_id, name, department, position, email, phone, leave_entitlement
    )
    if success:
        return f"✅ Employee {name} added successfully!"
    else:
        return f"❌ Failed to add employee {name}"

@mcp.tool()
def apply_leave(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str = ""
) -> str:
    """Apply for leave for an employee"""
    success = leave_mgr.apply_leave(
        employee_id, leave_type, start_date, end_date, reason
    )
    if success:
        return "✅ Leave request submitted successfully!"
    else:
        return "❌ Failed to submit leave request"

@mcp.tool()
def approve_leave(
    request_id: str,
    approver: str,
    status: str,
    comments: str = ""
) -> str:
    """Approve or reject a leave request"""
    success = leave_mgr.approve_leave(
        request_id, approver, status, comments
    )
    if success:
        return f"✅ Leave request {request_id} {status.lower()}"
    else:
        return f"❌ Failed to {status.lower()} leave request"

@mcp.tool()
def view_leave_requests(
    employee_id: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """View leave requests with optional filtering"""
    requests = leave_mgr.get_leave_requests(
        employee_id=employee_id, status=status
    )
    if not requests:
        return "No leave requests found."
    
    result = "📝 **LEAVE REQUESTS**\n\n"
    for req in requests:
        status_icon = "✅" if req['status'] == 'Approved' else "⏳" if req['status'] == 'Pending' else "❌"
        result += f"{status_icon} **{req['request_id']}**\n"
        result += f"  Employee: {req['employee_name']}\n"
        result += f"  Leave Type: {req['leave_type']}\n"
        result += f"  Dates: {req['start_date']} to {req['end_date']} ({req['total_days']} days)\n"
        result += f"  Status: {req['status']}\n"
        if req['reason']:
            result += f"  Reason: {req['reason']}\n"
        result += "\n"
    return result

@mcp.tool()
def view_leave_balance(employee_id: Optional[str] = None) -> str:
    """View leave balance for employees"""
    balances = leave_mgr.get_leave_balance(employee_id=employee_id)
    if not balances:
        return "No leave balance found."
    
    result = "💰 **LEAVE BALANCE**\n\n"
    for balance in balances:
        result += f"**{balance['employee_name']}** - {balance['leave_type']}\n"
        result += f"  Total: {balance['total_entitlement']} days\n"
        result += f"  Used: {balance['used_leaves']} days\n"
        result += f"  Remaining: {balance['remaining_leaves']} days\n\n"
    return result

@mcp.tool()
def get_leave_summary(year: Optional[int] = None) -> str:
    """Get leave summary for a specific year"""
    summary = leave_mgr.get_leave_summary(year)
    if not summary:
        return f"No data found for year {year or 'current year'}."
    
    result = f"📊 **LEAVE SUMMARY FOR {summary['year']}**\n\n"
    result += f"Total Requests: {summary['total_requests']}\n"
    result += f"Approved: {summary['approved_requests']}\n"
    result += f"Pending: {summary['pending_requests']}\n"
    result += f"Rejected: {summary['rejected_requests']}\n"
    result += f"Total Days Requested: {summary['total_days_requested']}\n"
    result += f"Total Days Approved: {summary['total_days_approved']}\n"
    result += f"Approval Rate: {summary['approval_rate']}%\n"
    return result

@mcp.tool()
def cancel_leave(request_id: str, employee_id: str) -> str:
    """Cancel a leave request"""
    success = leave_mgr.cancel_leave(request_id, employee_id)
    if success:
        return f"✅ Leave request {request_id} cancelled successfully"
    else:
        return f"❌ Failed to cancel leave request"

if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()
