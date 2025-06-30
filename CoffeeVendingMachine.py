from threading import Lock, Thread
from typing import Dict

class Ingredient:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity
        self.lock = Lock()

    def update_quantity(self, amount: int):
        with self.lock:
            self.quantity += amount

    def use_quantity(self, amount: int) -> bool:
        with self.lock:
            if self.quantity >= amount:
                self.quantity -= amount
                return True
            return False

class Coffee:
    def __init__(self, name: str, price: float, recipe: Dict[str, int]):
        self.name = name
        self.price = price
        self.recipe = recipe

class Payment:
    def __init__(self, amount_paid: float):
        self.amount_paid = amount_paid

class CoffeeMachine:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.ingredients: Dict[str, Ingredient] = {
            "water": Ingredient("water", 1000),
            "milk": Ingredient("milk", 1000),
            "coffee": Ingredient("coffee", 500),
        }
        self.menu: Dict[str, Coffee] = {
            "espresso": Coffee("espresso", 2.0, {"water": 50, "coffee": 18}),
            "cappuccino": Coffee("cappuccino", 3.0, {"water": 50, "milk": 30, "coffee": 18}),
            "latte": Coffee("latte", 3.5, {"water": 30, "milk": 60, "coffee": 18})
        }
        self._initialized = True

    def display_menu(self):
        print("\nAvailable Coffees:")
        for name, coffee in self.menu.items():
            print(f"- {name.title()} (${coffee.price})")

    def has_enough_ingredients(self, coffee: Coffee) -> bool:
        return all(
            self.ingredients[ing].quantity >= amt for ing, amt in coffee.recipe.items()
        )

    def update_ingredients(self, coffee: Coffee):
        for ing, amt in coffee.recipe.items():
            self.ingredients[ing].use_quantity(amt)

    def make_coffee(self, coffee_name: str, payment: Payment):
        if coffee_name not in self.menu:
            print(f"{coffee_name} is not available.")
            return

        coffee = self.menu[coffee_name]
        if not self.has_enough_ingredients(coffee):
            print(f"Not enough ingredients for {coffee.name}.")
            return

        if payment.amount_paid < coffee.price:
            print(f"Insufficient payment for {coffee.name}. Price: ${coffee.price}")
            return

        change = payment.amount_paid - coffee.price
        self.update_ingredients(coffee)
        print(f"Dispensed {coffee.name}. Change: ${change:.2f}")

        for ing, item in self.ingredients.items():
            if item.quantity < 100:
                print(f"Warning: {ing} is running low.")

# Demo with concurrent requests
def simulate_user(machine: CoffeeMachine, coffee_name: str, amount: float):
    payment = Payment(amount)
    machine.make_coffee(coffee_name, payment)

if __name__ == "__main__":
    coffee_machine = CoffeeMachine()
    coffee_machine.display_menu()

    threads = [
        Thread(target=simulate_user, args=(coffee_machine, "espresso", 2.5)),
        Thread(target=simulate_user, args=(coffee_machine, "latte", 4.0)),
        Thread(target=simulate_user, args=(coffee_machine, "cappuccino", 3.0)),
        Thread(target=simulate_user, args=(coffee_machine, "espresso", 1.5))
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
