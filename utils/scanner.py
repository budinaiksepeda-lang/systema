#scanner.py
import cv2
from pyzbar.pyzbar import decode
import threading
import time
import keyboard  # For USB scanner emulating keyboard

class QRScanner:
    def __init__(self, scanner_type="auto"):
        """
        scanner_type: "camera", "keyboard", or "auto"
        """
        self.scanner_type = scanner_type
        self.callback = None
        self.scanning = False
        
    def start_scanning(self, callback):
        """Start scanning for QR codes"""
        self.callback = callback
        
        if self.scanner_type in ["auto", "keyboard"]:
            # Try keyboard input first (USB scanner)
            self.start_keyboard_scanner()
        
        if self.scanner_type in ["auto", "camera"]:
            # Also start camera scanner
            self.start_camera_scanner()
    
    def start_keyboard_scanner(self):
        """Listen for keyboard input (USB barcode scanner)"""
        def keyboard_listener():
            buffer = ""
            while self.scanning:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'enter':
                        if buffer:
                            self.callback(buffer.strip())
                            buffer = ""
                    elif len(event.name) == 1:
                        buffer += event.name
                time.sleep(0.01)
        
        self.scanning = True
        thread = threading.Thread(target=keyboard_listener)
        thread.daemon = True
        thread.start()
    
    def start_camera_scanner(self):
        """Use camera to scan QR codes"""
        def camera_scanner():
            cap = cv2.VideoCapture(0)
            
            while self.scanning:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Decode QR codes
                decoded_objects = decode(frame)
                
                for obj in decoded_objects:
                    data = obj.data.decode('utf-8')
                    self.callback(data)
                
                # Show camera preview (optional)
                cv2.imshow('QR Scanner', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
        
        self.scanning = True
        thread = threading.Thread(target=camera_scanner)
        thread.daemon = True
        thread.start()
    
    def stop_scanning(self):
        """Stop all scanning processes"""
        self.scanning = False