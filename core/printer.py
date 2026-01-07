#printer.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from datetime import datetime
import os

class ReceiptPrinter:
    def __init__(self, company_info=None):
        self.company_info = company_info or {
            'name': 'TOKO XYZ',
            'address': 'Jl. Contoh No. 123',
            'phone': '(021) 12345678',
            'footer': 'Terima kasih telah berbelanja'
        }
        
    def generate_receipt(self, transaction_data, output_file="receipt.pdf"):
        """Generate precise receipt with proper formatting"""
        
        doc = SimpleDocTemplate(
            output_file,
            pagesize=(80*mm, 297*mm),  # Thermal printer size
            rightMargin=2*mm,
            leftMargin=2*mm,
            topMargin=2*mm,
            bottomMargin=2*mm
        )
        
        story = []
        styles = self.get_styles()
        
        # Company header
        story.append(Paragraph(self.company_info['name'], styles['Company']))
        story.append(Paragraph(self.company_info['address'], styles['NormalCenter']))
        story.append(Paragraph(self.company_info['phone'], styles['NormalCenter']))
        story.append(Spacer(1, 2*mm))
        
        # Separator line
        story.append(Paragraph("="*40, styles['NormalCenter']))
        
        # Transaction info
        trans_info = [
            f"Tanggal: {transaction_data['date']}",
            f"Kasir: {transaction_data['cashier']}",
            f"No. Transaksi: {transaction_data['transaction_code']}"
        ]
        
        for info in trans_info:
            story.append(Paragraph(info, styles['Normal']))
        
        story.append(Spacer(1, 2*mm))
        
        # Items table
        items_data = [['Item', 'Qty', 'Harga', 'Total']]
        
        for item in transaction_data['items']:
            items_data.append([
                item['name'][:20],  # Limit name length
                str(item['quantity']),
                f"Rp {item['price']:,.0f}",
                f"Rp {item['subtotal']:,.0f}"
            ])
        
        items_table = Table(items_data, colWidths=[30*mm, 10*mm, 20*mm, 20*mm])
        items_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 2*mm))
        
        # Summary
        summary_data = [
            ['Subtotal:', f"Rp {transaction_data['subtotal']:,.0f}"],
            ['Diskon:', f"-Rp {transaction_data['discount']:,.0f}"],
            ['Pajak (10%):', f"Rp {transaction_data['tax']:,.0f}"],
            ['', ''],
            ['TOTAL:', f"Rp {transaction_data['total']:,.0f}"],
            ['Tunai:', f"Rp {transaction_data['cash']:,.0f}"],
            ['Kembali:', f"Rp {transaction_data['change']:,.0f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[40*mm, 40*mm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 4), (-1, 4), 10),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 4), (-1, 4), 1, colors.black),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 5*mm))
        
        # Footer
        story.append(Paragraph(self.company_info['footer'], styles['NormalCenter']))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph("Barang yang sudah dibeli tidak dapat dikembalikan", 
                             styles['SmallCenter']))
        
        # Build PDF
        doc.build(story)
        
        return output_file
    
    def print_receipt(self, receipt_file, printer_name=None):
        """Print receipt to thermal printer"""
        import win32api  # For Windows
        import win32print
        
        if printer_name:
            # Use specific printer
            win32api.ShellExecute(
                0,
                "print",
                receipt_file,
                f'/d:"{printer_name}"',
                ".",
                0
            )
        else:
            # Use default printer
            win32api.ShellExecute(
                0,
                "print",
                receipt_file,
                None,
                ".",
                0
            )
    
    def get_styles(self):
        """Define styles for receipt"""
        styles = getSampleStyleSheet()
        
        custom_styles = {
            'Company': ParagraphStyle(
                'Company',
                parent=styles['Normal'],
                fontSize=12,
                alignment=1,  # Center
                fontName='Helvetica-Bold',
                spaceAfter=2
            ),
            'NormalCenter': ParagraphStyle(
                'NormalCenter',
                parent=styles['Normal'],
                alignment=1,
                fontSize=8
            ),
            'SmallCenter': ParagraphStyle(
                'SmallCenter',
                parent=styles['Normal'],
                alignment=1,
                fontSize=7,
                textColor=colors.grey
            )
        }
        
        return custom_styles