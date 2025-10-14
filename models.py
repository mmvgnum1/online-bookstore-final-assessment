class Book:
    def __init__(self, title, category, price, image):
        self.title = title
        self.category = category
        self.price = price
        self.image = image


class CartItem:
    def __init__(self, book, quantity=1):
        self.book = book
        self.quantity = quantity
    
    def get_total_price(self):
        return self.book.price * self.quantity


class Cart:
    """
    A shopping cart class that holds book items and their quantities.

    The Cart uses a dictionary with book titles as keys for efficient lookups,
    allowing operations like adding, removing, and updating book quantities.

    Attributes:
        items (dict): Dictionary storing CartItem objects with book titles as keys.

    Methods:
        add_book(book, quantity=1): Add a book to the cart with specified quantity.
        remove_book(book_title): Remove a book from the cart by title.
        update_quantity(book_title, quantity): Update quantity of a book in the cart.
        get_total_price(): Calculate total price of all items in the cart.
        get_total_items(): Get the total count of all books in the cart.
        clear(): Remove all items from the cart.
        get_items(): Return a list of all CartItem objects in the cart.
        is_empty(): Check if the cart has no items.
    """
    def __init__(self):
        self.items = {}  # Using dict with book title as key for easy lookup

    def add_book(self, book, quantity=1):
        if book.title in self.items:
            self.items[book.title].quantity += quantity
        else:
            self.items[book.title] = CartItem(book, quantity)

    def remove_book(self, book_title):
        if book_title in self.items:
            del self.items[book_title]

    def update_quantity(self, book_title, quantity):
        """Update quantity; remove if quantity <= 0. Coerce to int safely."""
        if book_title in self.items:
            try:
                q = int(quantity)
            except (TypeError, ValueError):
                # Invalid input -> treat as no-op
                return
            if q <= 0:
                del self.items[book_title]
            else:
                self.items[book_title].quantity = q




    def get_total_price(self):
        # O(n) instead of O(n*m)
        return sum(item.book.price * item.quantity for item in self.items.values())


    def get_total_items(self):
        return sum(item.quantity for item in self.items.values())

    def clear(self):
        self.items = {}

    def get_items(self):
        return list(self.items.values())

    def is_empty(self):
        return len(self.items) == 0


class User:
    """User account management class"""
    def __init__(self, email, password, name="", address=""):
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.orders = []
        """ Removed unused attributes to reduce memory/complexity 
        self.temp_data = []
        self.cache = {} """
    
    def add_order(self, order):
        # Append only; sort on demand if needed (YAGNI)
        self.orders.append(order)
    
    def get_order_history(self):
        # Return original list (read-only by convention for templates)
        return self.orders


class Order:
    """Order management class"""
    def __init__(self, order_id, user_email, items, shipping_info, payment_info, total_amount):
        import datetime
        self.order_id = order_id
        self.user_email = user_email
        self.items = items.copy()  # Copy of cart items
        self.shipping_info = shipping_info
        self.payment_info = payment_info
        self.total_amount = total_amount
        self.order_date = datetime.datetime.now()
        self.status = "Confirmed"
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_email': self.user_email,
            'items': [{'title': item.book.title, 'quantity': item.quantity, 'price': item.book.price} for item in self.items],
            'shipping_info': self.shipping_info,
            'total_amount': self.total_amount,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }


class PaymentGateway:
    """Mock payment gateway for processing payments"""
    
    @staticmethod
    def process_payment(payment_info):
        """Mock payment processing - returns success/failure with mock logic"""
        payment_method = (payment_info.get('payment_method') or '').lower()
        card_number = (payment_info.get('card_number') or '')
        expiry = (payment_info.get('expiry_date') or '')
        cvv = (payment_info.get('cvv') or '')
        
        # Mock logic: cards ending in '1111' fail, others succeed
        if card_number.endswith('1111'):
            return {
                'success': False,
                'message': 'Payment failed: Invalid card number',
                'transaction_id': None
            }
        
        """ CODE REMOVED BELOW
        import random
        import time
        import datetime 
        
        time.sleep(0.1) """
        
        # NEW CODE BELOW
        # Very light validation for demo purposes
        if payment_method == 'credit_card':
            # Trivial format checks to support tests
            if not (card_number and expiry and cvv):
                return {'success': False, 'message': 'Missing credit card details', 'transaction_id': None}
        elif payment_method == 'paypal':
            # In a real app: validate PayPal token/email. Here just accept presence.
            pass
        else:
            return {'success': False, 'message': 'Unsupported payment method', 'transaction_id': None}

        # (Keep imports top-level ideally; tiny delay retained but reduced)
        import random, time
        time.sleep(0.02)


        
        transaction_id = f"TXN{random.randint(100000, 999999)}"
        
        """"" Paypal path already implicitly accepted above. See below code removed.
        
        if payment_info.get('payment_method') == 'paypal':
            pass """""
        
        return {
            'success': True,
            'message': 'Payment processed successfully',
            'transaction_id': transaction_id
        }


class EmailService:
    """Mock email service for sending order confirmations"""
    
    @staticmethod
    def send_order_confirmation(user_email, order):
        """Mock email sending - just prints to console in this implementation"""
        print(f"\n=== EMAIL SENT ===")
        print(f"To: {user_email}")
        print(f"Subject: Order Confirmation - Order #{order.order_id}")
        print(f"Order Date: {order.order_date}")
        print(f"Total Amount: ${order.total_amount:.2f}")
        print(f"Items:")
        for item in order.items:
            print(f"  - {item.book.title} x{item.quantity} @ ${item.book.price:.2f}")
        print(f"Shipping Address: {order.shipping_info.get('address', 'N/A')}")
        print(f"==================\n")
        
        return True
