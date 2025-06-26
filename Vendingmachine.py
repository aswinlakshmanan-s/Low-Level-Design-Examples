# ----------------------------------------
# ✅ GOAL:
# Design a Vending Machine that:
# - Lets user select item
# - Accepts money
# - Dispenses item & returns change
# - Resets after each purchase
# - Handles out-of-stock or errors gracefully
# ----------------------------------------

# ✅ Design Pattern Used: STATE PATTERN
# - Machine behavior changes depending on its current state
# - Good alternative to long if-else/switch blocks
# - Makes code clean, maintainable, and extendable
# ----------------------------------------

# ✅ CLASSES BREAKDOWN:

# 1️⃣ Item
# - Represents a product (e.g., Coke, Chips)
# - Has name and price

# 2️⃣ Inventory
# - Tracks stock for each item
# - Contains logic to decrease quantity

# 3️⃣ VendingMachineState (Abstract Class)
# - Blueprint for states (NoMoney, HasMoney)
# - Each state must handle:
#     - select_item()
#     - insert_money()
#     - dispense_item()

# 4️⃣ NoMoneyState
# - Waiting for user to select an item
# - After selection, moves to HasMoneyState

# 5️⃣ HasMoneyState
# - Waiting for enough money to be inserted
# - Dispenses item if funds are enough
# - Returns change if needed
# - Resets state back to NoMoney after transaction

# 6️⃣ VendingMachine
# - Main controller
# - Has current state
# - Delegates all actions to state
# - Handles inventory, inserted money, and transitions

# 7️⃣ main()
# - Simulates a real user using the vending machine
# - Demonstrates all flows: success, partial money, change, out of stock

# ----------------------------------------
# ✅ KEY OBJECT-ORIENTED PRINCIPLES USED:

# - Encapsulation: Each class does one job (e.g., Item handles name/price only)
# - Polymorphism: Different states behave differently for the same action
# - Open/Closed Principle: Easy to add more states (like MaintenanceState) without changing existing logic
# ----------------------------------------

# ✅ INTERVIEW TIPS:
# - Mention "State Pattern" early
# - Explain each class's role clearly
# - Show how transitions are clean (set_state)
# - Mention extensibility: can easily add Cancel/Refund, Card Payments, MaintenanceMode
# ----------------------------------------



from abc import ABC, abstractmethod

# -------------------- ITEM & INVENTORY --------------------

class Item:
    """Represents a snack item in the machine."""
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Inventory:
    """Tracks quantity of a specific item."""
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
        else:
            raise ValueError("Item is out of stock.")

# -------------------- STATE TEMPLATE --------------------

class VendingMachineState(ABC):
    """All states must handle selection, payment, and dispensing."""
    @abstractmethod
    def select_item(self, machine, item_name: str):
        pass

    @abstractmethod
    def insert_money(self, machine, amount: float):
        pass

    @abstractmethod
    def dispense_item(self, machine):
        pass

# -------------------- NO MONEY STATE --------------------

class NoMoneyState(VendingMachineState):
    def select_item(self, machine, item_name: str):
        print(f"Selected {item_name}. Please insert money.")
        machine.selected_item_name = item_name
        machine.set_state(HasMoneyState())

    def insert_money(self, machine, amount: float):
        print("Please select an item first.")

    def dispense_item(self, machine):
        print("Please select an item and insert money first.")

# -------------------- HAS MONEY STATE --------------------

class HasMoneyState(VendingMachineState):
    def select_item(self, machine, item_name: str):
        print(f"Already processing selection: {machine.selected_item_name}. Please complete or cancel it.")

    def insert_money(self, machine, amount: float):
        machine.inserted_money += amount
        print(f"Inserted ${amount:.2f}. Total: ${machine.inserted_money:.2f}")

        selected_inventory = machine.inventory.get(machine.selected_item_name)
        if not selected_inventory:
            print("Error: Item not found.")
            machine.eject_money()
            return

        if machine.inserted_money >= selected_inventory.item.price:
            self.dispense_item(machine)
        else:
            needed = selected_inventory.item.price - machine.inserted_money
            print(f"Please insert ${needed:.2f} more.")

    def dispense_item(self, machine):
        selected_inventory = machine.inventory.get(machine.selected_item_name)
        try:
            selected_inventory.decrease_quantity()
            change = machine.inserted_money - selected_inventory.item.price
            print(f"Dispensing {machine.selected_item_name}.")
            if change > 0:
                print(f"Returning change: ${change:.2f}")
            machine.reset()
        except ValueError as e:
            print(str(e))
            machine.eject_money()

# -------------------- VENDING MACHINE --------------------

class VendingMachine:
    """Main vending machine logic."""
    def __init__(self):
        self.inventory = {}              # Holds all items
        self.state = NoMoneyState()      # Starts in idle mode
        self.inserted_money = 0.0
        self.selected_item_name = None

    def load_inventory(self, item: Item, quantity: int):
        self.inventory[item.name] = Inventory(item, quantity)
        print(f"Loaded {quantity} of {item.name}.")

    def set_state(self, state: VendingMachineState):
        self.state = state

    def select_item(self, item_name: str):
        self.state.select_item(self, item_name)

    def insert_money(self, amount: float):
        self.state.insert_money(self, amount)

    def eject_money(self):
        print(f"Ejecting ${self.inserted_money:.2f}")
        self.reset()

    def reset(self):
        self.inserted_money = 0.0
        self.selected_item_name = None
        self.set_state(NoMoneyState())

# -------------------- MAIN FUNCTION --------------------

def main():
    vm = VendingMachine()

    # Load some snacks into the machine
    vm.load_inventory(Item("Coke", 2.50), 3)
    vm.load_inventory(Item("Chips", 1.75), 2)
    vm.load_inventory(Item("Water", 1.00), 5)

    print("\n--- Scenario 1: Buy Coke ---")
    vm.select_item("Coke")
    vm.insert_money(1.00)
    vm.insert_money(1.50)

    print("\n--- Scenario 2: Select Chips but Cancel ---")
    vm.select_item("Chips")
    vm.eject_money()

    print("\n--- Scenario 3: Not Enough Money ---")
    vm.select_item("Chips")
    vm.insert_money(1.00)

    print("\n--- Scenario 4: Complete Chips Purchase ---")
    vm.insert_money(0.75)

    print("\n--- Scenario 5: Try Selecting While Mid-Transaction ---")
    vm.select_item("Coke")
    vm.insert_money(5.00)
    vm.select_item("Water")  # Should say: already selected Coke

# Run the code
if __name__ == "__main__":
    main()
