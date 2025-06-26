"""
Pizza Ordering System - Low Level Design

Design Overview:
----------------
This system models a Pizza Ordering system using Object-Oriented Design principles and the Builder Pattern.

Key Concepts:
-------------
1. Enums (Size, Crust, Topping):
   - Define fixed choices for pizza configuration (strong typing).
   - Each enum value includes both a price and a user-friendly description.
   - Enums ensure readability, extensibility, and avoid magic strings.

2. Pizza Class:
   - Represents a single pizza object composed of size, crust, and toppings.
   - Provides methods for price calculation and string representation.
   - Designed to be immutable after construction (no direct setters).

3. Builder Pattern (Nested in Pizza):
   - Allows for step-by-step pizza construction using a fluent interface.
   - Ensures required fields (size, crust) are validated before creation.
   - Prevents constructor overloading or long argument lists.

4. Order Class:
   - Acts as a container for multiple pizzas (cart-like behavior).
   - Aggregates total cost and prints a clean receipt.
   - Can be extended to include coupons, customer info, or delivery logic.

Design Principles Applied:
--------------------------
- **Single Responsibility**: Each class has one job (Pizza, Builder, Order).
- **Open/Closed Principle**: New toppings or sizes can be added without changing existing code.
- **Encapsulation**: Internal details (like price logic) are hidden from the user.
- **Extensibility**: Easy to add new pizza types, features, or export APIs in the future.
- **Fluent Interface**: Improves readability and mimics real-world configuration flow.

Use Case:
---------
This design simulates real-world pizza ordering flow like Domino’s or Pizza Hut:
- Customer picks pizza size and crust.
- Adds one or more toppings.
- System calculates the price.
- Multiple pizzas can be grouped into a single order.

Future Enhancements (Easy to Plug In):
--------------------------------------
- Add pizza size-based discounts or combo pricing.
- Add customer profiles and delivery tracking.
- Convert to REST API for online ordering system.
- Add persistent storage (DB/file).
- Integrate invoice generation (PDF/email).

Overall:
--------
This is a clean, scalable, and extensible object-oriented design suitable for backend applications, e-commerce systems, or microservice endpoints for food delivery platforms.
"""

from enum import Enum
from typing import List, Set

# Step 1: Define Enums for Size, Crust, and Toppings

class Size(Enum):
    SMALL = (8.00, "Small")
    MEDIUM = (10.00, "Medium")
    LARGE = (12.00, "Large")
    
    def __init__(self, price, description):
        self.price = price
        self.description = description

class Crust(Enum):
    THIN = (2.00, "Thin Crust")
    HAND_TOSSED = (2.50, "Hand-Tossed")
    DEEP_DISH = (3.50, "Deep Dish")
    
    def __init__(self, price, description):
        self.price = price
        self.description = description

class Topping(Enum):
    PEPPERONI = (1.50, "Pepperoni")
    MUSHROOMS = (1.00, "Mushrooms")
    ONIONS = (0.75, "Onions")
    EXTRA_CHEESE = (2.00, "Extra Cheese")
    TOMATO_SAUCE = (0.50, "Tomato Sauce")
    BASIL = (0.75, "Basil")
    
    def __init__(self, price, description):
        self.price = price
        self.description = description

# Step 2: Define the Pizza class
class Pizza:
    def __init__(self, builder):
        self.size: Size = builder.size
        self.crust: Crust = builder.crust
        self.toppings: Set[Topping] = set(builder.toppings)  # defensive copy

    def calculate_price(self) -> float:
        price = self.size.price + self.crust.price
        price += sum(topping.price for topping in self.toppings)
        return round(price, 2)

    def __str__(self) -> str:
        description = f"- {self.size.description} {self.crust.description} Pizza (${self.calculate_price():.2f})\n"
        if self.toppings:
            description += "  Toppings: " + ", ".join(
                t.description for t in sorted(list(self.toppings), key=lambda t: t.name)
            )
        return description

    # Step 3: Builder Class
    class Builder:
        def __init__(self):
            self.size: Size = None
            self.crust: Crust = None
            self.toppings: Set[Topping] = set()

        def with_size(self, size: Size):
            self.size = size
            return self

        def with_crust(self, crust: Crust):
            self.crust = crust
            return self

        def add_topping(self, topping: Topping):
            self.toppings.add(topping)
            return self

        def remove_topping(self, topping: Topping):
            self.toppings.discard(topping)
            return self

        def build(self) -> 'Pizza':
            if not self.size or not self.crust:
                raise ValueError("A pizza must have a size and a crust.")
            return Pizza(self)

# Step 4: Order Class
class Order:
    def __init__(self, order_id: int):
        self.order_id = order_id
        self.items: List[Pizza] = []

    def add_item(self, item: Pizza):
        self.items.append(item)

    def calculate_total(self) -> float:
        return round(sum(item.calculate_price() for item in self.items), 2)

    def print_receipt(self):
        print(f"--- Order #{self.order_id} ---")
        if not self.items:
            print("Order is empty.")
        else:
            for item in self.items:
                print(str(item))
        print("--------------------")
        print(f"Total: ${self.calculate_total():.2f}")
        print("--------------------")

# Step 5: Main function to simulate a pizza order
def main():
    order = Order(order_id=101)

    # Pizza 1
    print("\nBuilding Pizza 1...")
    pizza1 = Pizza.Builder()\
        .with_size(Size.LARGE)\
        .with_crust(Crust.DEEP_DISH)\
        .add_topping(Topping.PEPPERONI)\
        .add_topping(Topping.MUSHROOMS)\
        .add_topping(Topping.ONIONS)\
        .build()
    order.add_item(pizza1)

    # Pizza 2
    print("\nBuilding Pizza 2...")
    pizza2 = Pizza.Builder()\
        .with_size(Size.MEDIUM)\
        .with_crust(Crust.THIN)\
        .add_topping(Topping.EXTRA_CHEESE)\
        .add_topping(Topping.TOMATO_SAUCE)\
        .build()
    order.add_item(pizza2)

    # Print Final Receipt
    print("\nFinal Order Receipt:")
    order.print_receipt()

if __name__ == "__main__":
    main()

