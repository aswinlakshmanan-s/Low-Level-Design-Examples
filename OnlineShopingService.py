from typing import List, Dict
from enum import Enum
import uuid

# Product Category
class Category(Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    BOOKS = "Books"
    HOME = "Home"

# Product
class Product:
    def __init__(self, product_id: str, name: str, price: float, category: Category, quantity: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity

# Inventory Manager
class InventoryManager:
    def __init__(self):
        self.products: Dict[str, Product] = {}

    def add_product(self, product: Product):
        self.products[product.product_id] = product

    def search_by_name(self, name: str) -> List[Product]:
        return [p for p in self.products.values() if name.lower() in p.name.lower()]

    def get_by_category(self, category: Category) -> List[Product]:
        return [p for p in self.products.values() if p.category == category]

    def is_available(self, product_id: str, quantity: int) -> bool:
        return self.products[product_id].quantity >= quantity

    def reduce_stock(self, product_id: str, quantity: int):
        self.products[product_id].quantity -= quantity

# Cart
class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

class Cart:
    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, product: Product, quantity: int):
        self.items.append(CartItem(product, quantity))

    def clear(self):
        self.items.clear()

# Order
class OrderStatus(Enum):
    PLACED = "Placed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

class Order:
    def __init__(self, user_id: str, cart_items: List[CartItem], total: float):
        self.order_id = str(uuid.uuid4())
        self.user_id = user_id
        self.items = cart_items
        self.total = total
        self.status = OrderStatus.PLACED

# Payment
class PaymentMethod(Enum):
    CARD = "Card"
    UPI = "UPI"
    COD = "Cash on Delivery"

class PaymentService:
    def pay(self, amount: float, method: PaymentMethod) -> bool:
        print(f"Payment of ${amount:.2f} using {method.value} successful.")
        return True

# User
class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.cart = Cart()
        self.orders: List[Order] = []

    def view_orders(self):
        return self.orders

# Online Shopping System (Putting all together)
class OnlineShoppingSystem:
    def __init__(self):
        self.inventory = InventoryManager()
        self.users: Dict[str, User] = {}

    def register_user(self, name: str) -> User:
        user_id = str(uuid.uuid4())
        user = User(user_id, name)
        self.users[user_id] = user
        return user

    def browse_category(self, category: Category):
        return self.inventory.get_by_category(category)

    def search_products(self, keyword: str):
        return self.inventory.search_by_name(keyword)

    def place_order(self, user: User, payment_method: PaymentMethod):
        total = sum(item.product.price * item.quantity for item in user.cart.items)
        for item in user.cart.items:
            if not self.inventory.is_available(item.product.product_id, item.quantity):
                print(f"Insufficient stock for {item.product.name}")
                return None

        payment_success = PaymentService().pay(total, payment_method)
        if payment_success:
            for item in user.cart.items:
                self.inventory.reduce_stock(item.product.product_id, item.quantity)

            order = Order(user.user_id, user.cart.items.copy(), total)
            user.orders.append(order)
            user.cart.clear()
            print(f"Order placed successfully with ID {order.order_id}")
            return order
        return None
