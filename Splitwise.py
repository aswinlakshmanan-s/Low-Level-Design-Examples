from typing import Dict, List

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

class Expense:
    def __init__(self, paid_by: str, amount: float, participants: List[str], splits: Dict[str, float]):
        self.paid_by = paid_by
        self.amount = amount
        self.participants = participants
        self.splits = splits  # How much each person owes

class Splitwise:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.balances: Dict[str, Dict[str, float]] = {}  # balances[A][B] = B owes A

    def add_user(self, user_id: str, name: str):
        self.users[user_id] = User(user_id, name)
        self.balances[user_id] = {}

    def add_expense(self, paid_by: str, amount: float, participants: List[str], splits: Dict[str, float]):
        expense = Expense(paid_by, amount, participants, splits)
        for user, split_amount in splits.items():
            if user == paid_by:
                continue
            self._add_to_balance(paid_by, user, split_amount)

    def _add_to_balance(self, paid_by: str, owes: str, amount: float):
        self.balances[paid_by][owes] = self.balances[paid_by].get(owes, 0) + amount
        self.balances[owes][paid_by] = self.balances[owes].get(paid_by, 0) - amount

    def show_balances(self):
        printed = set()
        for user1 in self.users:
            for user2 in self.balances[user1]:
                if self.balances[user1][user2] > 0 and (user1, user2) not in printed:
                    print(f"{self.users[user2].name} owes {self.users[user1].name}: ${self.balances[user1][user2]:.2f}")
                    printed.add((user1, user2))
                    printed.add((user2, user1))

# -------- Sample Usage --------
if __name__ == "__main__":
    app = Splitwise()

    # Adding users
    app.add_user("u1", "Alice")
    app.add_user("u2", "Bob")
    app.add_user("u3", "Charlie")

    # Expense 1: Alice paid $120, split equally among Alice, Bob, Charlie
    equal_split = {"u1": 40.0, "u2": 40.0, "u3": 40.0}
    app.add_expense("u1", 120.0, ["u1", "u2", "u3"], equal_split)

    # Expense 2: Bob paid $60, split as: Bob 30, Charlie 30
    custom_split = {"u2": 30.0, "u3": 30.0}
    app.add_expense("u2", 60.0, ["u2", "u3"], custom_split)

    app.show_balances()
