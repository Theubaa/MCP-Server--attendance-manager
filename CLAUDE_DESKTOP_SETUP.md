# 🚀 Claude Desktop Setup for Leave Management System

## ✅ **Your MCP Server is Ready!**

The leave management system has been successfully converted to a FastMCP server that Claude Desktop can use.

## 🔧 **Setup Instructions:**

### **1. Copy Configuration to Claude Desktop:**

In Claude Desktop, go to **Settings > MCP Servers** and add this configuration:

```json
{
  "mcpServers": {
    "leave-management": {
      "command": "C:/Users/team/AppData/Local/Programs/Python/Python310/python.exe",
      "args": ["C:/Users/team/OneDrive/Desktop/MCP/my-first-mcp-server/mcp_server.py"],
      "cwd": "C:/Users/team/OneDrive/Desktop/MCP/my-first-mcp-server"
    }
  }
}
```

**Important:** Use the **FULL ABSOLUTE PATH** for the `args` parameter as shown above.

### **2. Available Tools:**

Once connected, Claude will have access to these tools:

- **`view_employees`** - See all employees in the system
- **`add_employee`** - Add new team members
- **`apply_leave`** - Submit leave requests
- **`approve_leave`** - Approve/reject leaves
- **`view_leave_requests`** - Check leave status
- **`view_leave_balance`** - See remaining leaves
- **`get_leave_summary`** - Annual statistics
- **`cancel_leave`** - Cancel requests

### **3. Example Claude Commands:**

```
"Show me all employees in the system"
"Add a new developer named Alex with ID EMP006"
"Apply for 5 days annual leave for vibhanshu starting next month"
"Show me the leave balance for all employees"
"Get the leave summary for 2025"
"Approve the leave request for LR001"
```

## 🎯 **What You've Built:**

1. **Complete Leave Management System** - Full functionality with 8 tools
2. **FastMCP Server** - Claude Desktop compatible
3. **Mock Data** - 5 employees ready to use
4. **Professional Code** - Production-ready quality

## 🔍 **Troubleshooting:**

- **Server not found**: Make sure the Python path is correct
- **File not found error**: Use the FULL ABSOLUTE PATH in the `args` parameter
- **Tools not showing**: Restart Claude Desktop after adding the MCP server
- **Connection errors**: Verify the working directory path exists

## 🎉 **You're All Set!**

Your leave management system is now ready to use with Claude Desktop. Claude will be able to manage your team's leave requests through natural language commands!
