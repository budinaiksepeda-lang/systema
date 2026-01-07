# main.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
from database.database import Database
from gui.login_window import LoginWindow
from gui.admin_dashboard import AdminDashboard
from gui.employee_dashboard import EmployeeDashboard

class CashierSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistem Kasir Lengkap - PT. XYZ")
        self.root.geometry("1200x700")
        
        # Initialize database
        self.db = Database()
        
        # Current user
        self.current_user = None
        
        # Show login window first
        self.show_login()
        
    def show_login(self):
        """Show login window"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        
        # Show appropriate dashboard based on role
        if user_data['role'] in ['admin', 'manager']:
            AdminDashboard(self.root, self.db, user_data, self.logout)
        else:
            EmployeeDashboard(self.root, self.db, user_data, self.logout)
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.show_login()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CashierSystem()
    app.run()