# database/database.py
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import hashlib

class Database:
    def __init__(self, db_path="cashier_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabel Users dengan role-based permissions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'cashier')),
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Produk
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                category TEXT,
                purchase_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 10,
                barcode_data TEXT,
                qr_code_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel Transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_code TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                discount_amount REAL DEFAULT 0,
                discount_percentage REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                final_amount REAL NOT NULL,
                payment_method TEXT,
                cash_paid REAL,
                change_amount REAL,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Tabel Detail Transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                discount REAL DEFAULT 0,
                subtotal REAL NOT NULL,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        # Tabel Void Transactions (Hanya admin/manager)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS void_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_transaction_id INTEGER NOT NULL,
                voided_by INTEGER NOT NULL,
                reason TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (original_transaction_id) REFERENCES transactions(id),
                FOREIGN KEY (voided_by) REFERENCES users(id)
            )
        ''')
        
        # Tabel Inventory Log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                quantity_change INTEGER NOT NULL,
                previous_stock INTEGER NOT NULL,
                new_stock INTEGER NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Insert admin default jika belum ada
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        if cursor.fetchone()[0] == 0:
            admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin', admin_hash, 'Administrator', 'admin'))
        
        conn.commit()
        conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    # ... tambahkan method lainnya untuk CRUD operations