# transaction.py
class TransactionCalculator:
    def __init__(self):
        pass
    
    def calculate_discount(self, subtotal, discount_type, discount_value):
        """
        Calculate discount with various types:
        - percentage: discount_value is percentage (0-100)
        - fixed: discount_value is fixed amount
        - buy_n_get_m: special promotion
        """
        if discount_type == 'percentage':
            if discount_value < 0 or discount_value > 100:
                raise ValueError("Persentase diskon harus antara 0-100")
            discount_amount = subtotal * (discount_value / 100)
        elif discount_type == 'fixed':
            discount_amount = min(discount_value, subtotal)
        elif discount_type == 'buy_n_get_m':
            # Special logic for buy N get M free
            discount_amount = self.calculate_buy_n_get_m(subtotal, discount_value)
        else:
            discount_amount = 0
        
        return discount_amount
    
    def calculate_buy_n_get_m(self, subtotal, promotion_rule):
        """
        Calculate buy N get M free discount
        promotion_rule format: "3:1" means buy 3 get 1 free
        """
        try:
            n, m = map(int, promotion_rule.split(':'))
            # Logic for this promotion
            # This would need actual cart items to calculate properly
            return 0  # Placeholder
        except:
            return 0
    
    def calculate_tax(self, subtotal, tax_percentage=10):
        """Calculate tax (PPN)"""
        return subtotal * (tax_percentage / 100)
    
    def calculate_final_amount(self, items, discount_type=None, discount_value=0):
        """
        Calculate final amount with all discounts and taxes
        """
        subtotal = sum(item['price'] * item['quantity'] for item in items)
        
        # Apply discount
        discount_amount = self.calculate_discount(subtotal, discount_type, discount_value)
        
        # Calculate taxable amount
        taxable_amount = subtotal - discount_amount
        
        # Calculate tax
        tax_amount = self.calculate_tax(taxable_amount)
        
        # Final amount
        final_amount = taxable_amount + tax_amount
        
        return {
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'taxable_amount': taxable_amount,
            'tax_amount': tax_amount,
            'final_amount': final_amount
        }