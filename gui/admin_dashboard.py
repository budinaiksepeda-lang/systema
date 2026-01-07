#admin_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import font as tkfont

class AdminDashboard:
    def __init__(self, root, db, user, logout_callback):
        self.root = root
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        
        self.setup_ui()
        self.load_dashboard_data()
    
    def setup_ui(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, 
                 text=f"Dashboard Admin - {self.user['full_name']}",
                 font=tkfont.Font(size=16, weight="bold"),
                 foreground="#2c3e50").pack(side=tk.LEFT)
        
        # Logout button
        ttk.Button(header_frame, text="Logout", 
                  command=self.logout_callback).pack(side=tk.RIGHT)
        
        # Navigation tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_transaction_tab()
        self.create_inventory_tab()
        self.create_void_tab()
        self.create_user_tab()
        self.create_report_tab()
    
    def create_dashboard_tab(self):
        """Create dashboard with statistics"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(dashboard_frame, text="Statistik Hari Ini")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create stats cards
        stats_data = self.get_today_stats()
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        metrics = [
            ("Total Penjualan", f"Rp {stats_data['total_sales']:,.0f}", "#27ae60"),
            ("Transaksi", str(stats_data['transaction_count']), "#2980b9"),
            ("Produk Terjual", str(stats_data['items_sold']), "#8e44ad"),
            ("Rata-rata Transaksi", f"Rp {stats_data['avg_transaction']:,.0f}", "#e67e22"),
            ("Stock Rendah", str(stats_data['low_stock']), "#e74c3c"),
            ("Profit", f"Rp {stats_data['profit']:,.0f}", "#16a085")
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            card = ttk.Frame(stats_grid, relief=tk.RAISED, borderwidth=1)
            card.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
            
            ttk.Label(card, text=label, font=("Arial", 10)).pack(pady=(10,0))
            ttk.Label(card, text=value, font=("Arial", 16, "bold"), 
                     foreground=color).pack(pady=(5,10))
        
        # Chart frame
        chart_frame = ttk.LabelFrame(dashboard_frame, text="Grafik Penjualan 7 Hari")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.create_sales_chart(chart_frame)
    
    def create_void_tab(self):
        """Tab khusus untuk void transaction (admin only)"""
        void_frame = ttk.Frame(self.notebook)
        self.notebook.add(void_frame, text="Void Transaction")
        
        # Search frame
        search_frame = ttk.Frame(void_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Cari Transaksi:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="Cari", 
                  command=self.search_transaction).pack(side=tk.LEFT)
        
        # Transaction list
        columns = ("ID", "Kode", "Tanggal", "Total", "Kasir", "Aksi")
        self.void_tree = ttk.Treeview(void_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.void_tree.heading(col, text=col)
            self.void_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(void_frame, orient=tk.VERTICAL, command=self.void_tree.yview)
        self.void_tree.configure(yscrollcommand=scrollbar.set)
        
        self.void_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Void form
        form_frame = ttk.LabelFrame(void_frame, text="Form Void")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Alasan Void:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reason_text = tk.Text(form_frame, height=4, width=40)
        self.reason_text.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Proses Void", 
                  command=self.process_void,
                  style="Danger.TButton").grid(row=1, column=1, pady=10, sticky=tk.E)
    
    def process_void(self):
        """Process void transaction"""
        selected = self.void_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih transaksi terlebih dahulu!")
            return
        
        reason = self.reason_text.get("1.0", tk.END).strip()
        if not reason:
            messagebox.showwarning("Peringatan", "Harap isi alasan void!")
            return
        
        # Confirm void
        if messagebox.askyesno("Konfirmasi", 
                               "Apakah Anda yakin ingin membatalkan transaksi ini?"):
            # Process void in database
            # ... implementation ...
            messagebox.showinfo("Sukses", "Transaksi berhasil dibatalkan!")
            self.search_transaction()
            self.reason_text.delete("1.0", tk.END)