#setup.py
"""
from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    "packages": ["tkinter", "PIL", "qrcode", "pyzbar", "cv2", 
                 "keyboard", "reportlab", "pandas", "matplotlib",
                 "sqlite3", "numpy"],
    "excludes": ["tkinter.test"],
    "include_files": [
        "database/",
        "config/",
        "qrcodes/"
    ],
    "optimize": 2
}

setup(
    name="Cashier System Pro",
    version="1.0.0",
    description="Sistem Kasir Lengkap dengan QR Code dan Inventory",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="icon.ico")]
)
"""