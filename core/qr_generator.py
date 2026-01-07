# qr_generator.py
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import pandas as pd

class QRGenerator:
    def __init__(self, output_dir="qrcodes"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_single_qr(self, product_data, include_price=True):
        """Generate single QR code with product information"""
        # Prepare data
        qr_data = {
            'code': product_data['code'],
            'name': product_data['name'],
            'price': product_data['selling_price']
        }
        
        # Convert to string
        data_string = f"PRODUCT:{qr_data['code']}|{qr_data['name']}|{qr_data['price']}"
        
        # Generate QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_string)
        qr.make(fit=True)
        
        # Create image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Add text below QR if needed
        if include_price:
            # Create larger canvas
            canvas = Image.new('RGB', (300, 350), 'white')
            canvas.paste(qr_img, (50, 20))
            
            # Add text
            draw = ImageDraw.Draw(canvas)
            
            # Load font (use default if not available)
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Product name
            draw.text((10, 280), product_data['name'][:30], fill="black", font=font)
            
            # Price
            price_text = f"Rp {product_data['selling_price']:,.0f}"
            draw.text((10, 310), price_text, fill="green", font=font)
            
            final_image = canvas
        else:
            final_image = qr_img
        
        # Save file
        filename = f"{product_data['code']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        final_image.save(filepath)
        
        return filepath
    
    def generate_bulk_qr(self, products_data, quantity_per_product=1):
        """Generate multiple QR codes in bulk"""
        generated_files = []
        
        for product in products_data:
            for i in range(quantity_per_product):
                filepath = self.generate_single_qr(product)
                generated_files.append({
                    'product_code': product['code'],
                    'product_name': product['name'],
                    'file_path': filepath,
                    'sequence': i + 1
                })
        
        # Create summary CSV
        summary_path = os.path.join(self.output_dir, 
                                  f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        df = pd.DataFrame(generated_files)
        df.to_csv(summary_path, index=False)
        
        return generated_files, summary_path
    
    def print_qr_codes(self, filepaths, printer_name=None):
        """Print QR codes to printer"""
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4, inch
        from reportlab.lib.units import mm
        
        # Create PDF for printing
        pdf_path = "qrcodes_to_print.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        
        width, height = A4
        
        # Layout: 3 columns, 10 rows
        x_margin = 15 * mm
        y_margin = 15 * mm
        qr_width = 60 * mm
        qr_height = 40 * mm
        
        x_positions = [x_margin, x_margin + qr_width + 5*mm, x_margin + 2*(qr_width + 5*mm)]
        y_positions = []
        
        current_y = height - y_margin
        for i in range(10):
            y_positions.append(current_y)
            current_y -= (qr_height + 5*mm)
        
        # Place QR codes
        for idx, filepath in enumerate(filepaths):
            if idx >= 30:  # Max per page
                c.showPage()
                idx = 0
            
            col = idx % 3
            row = idx // 3
            
            x = x_positions[col]
            y = y_positions[row]
            
            # Add QR image
            c.drawImage(filepath, x, y - qr_height, width=qr_width, height=qr_height)
        
        c.save()
        
        # Print PDF
        if printer_name:
            os.startfile(pdf_path, "print")
        
        return pdf_path