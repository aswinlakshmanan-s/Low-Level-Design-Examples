from threading import Lock, Thread
from typing import Dict, List

class InventoryService:
    def __init__(self):
        # This will store inventory in the format: inventory[seller_id][product_id] = quantity
        self.inventory: Dict[str, Dict[str, int]] = {}
        self.lock = Lock()  # One lock to protect access to inventory

    def add_inventory(self, seller_id: str, product_id: str, quantity: int):
        with self.lock:  # Lock while modifying the inventory
            if seller_id not in self.inventory:
                self.inventory[seller_id] = {}
            if product_id not in self.inventory[seller_id]:
                self.inventory[seller_id][product_id] = 0
            self.inventory[seller_id][product_id] += quantity
            print(f"Added {quantity} of {product_id} to seller {seller_id}. Now has {self.inventory[seller_id][product_id]}")

    def create_order(self, seller_id: str, product_id: str, quantity: int) -> bool:
        with self.lock:  # Lock while reading and writing inventory
            if seller_id in self.inventory and product_id in self.inventory[seller_id]:
                if self.inventory[seller_id][product_id] >= quantity:
                    self.inventory[seller_id][product_id] -= quantity
                    print(f"Order created for {quantity} of {product_id} from seller {seller_id}.")
                    return True
            print(f"Order failed for {quantity} of {product_id} from seller {seller_id}.")
            return False

    def get_available_inventory(self, seller_id: str, product_id: str) -> int:
        with self.lock:  # Lock while reading inventory
            return self.inventory.get(seller_id, {}).get(product_id, 0)

    def get_sellers_for_product(self, product_id: str, required_quantity: int) -> List[str]:
        eligible_sellers = []
        with self.lock:  # Lock while scanning all inventory
            for seller_id, products in self.inventory.items():
                if products.get(product_id, 0) >= required_quantity:
                    eligible_sellers.append(seller_id)
        return eligible_sellers

# --- Sample Usage ---

def simulate():
    service = InventoryService()

    # Adding inventory
    service.add_inventory("seller1", "apple", 50)
    service.add_inventory("seller2", "apple", 100)
    service.add_inventory("seller1", "banana", 30)

    # Creating orders
    service.create_order("seller1", "apple", 20)
    service.create_order("seller2", "apple", 150)  # Should fail

    # Checking available inventory
    print("Seller1 has:", service.get_available_inventory("seller1", "apple"), "apples")

    # Getting list of sellers who can fulfill 40 apples
    sellers = service.get_sellers_for_product("apple", 40)
    print("Sellers with >=40 apples:", sellers)

if __name__ == "__main__":
    simulate()
