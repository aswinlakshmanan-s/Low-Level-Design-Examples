from abc import ABC, abstractmethod
from threading import Lock

# Card class
class Card:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin

# Account class
class Account:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance
        self.lock = Lock()

    def debit(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False

    def credit(self, amount):
        with self.lock:
            self.balance += amount
            return True

    def get_balance(self):
        with self.lock:
            return self.balance

# Abstract Transaction class
class Transaction(ABC):
    @abstractmethod
    def execute(self):
        pass

# Withdrawal transaction
class WithdrawalTransaction(Transaction):
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def execute(self):
        return self.account.debit(self.amount)

# Deposit transaction
class DepositTransaction(Transaction):
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def execute(self):
        return self.account.credit(self.amount)

# BankingService
class BankingService:
    def __init__(self):
        self.accounts = {}
        self.lock = Lock()

    def add_account(self, account):
        with self.lock:
            self.accounts[account.account_number] = account

    def get_account(self, account_number):
        with self.lock:
            return self.accounts.get(account_number)

# CashDispenser
class CashDispenser:
    def __init__(self, initial_cash):
        self.cash_available = initial_cash
        self.lock = Lock()

    def dispense_cash(self, amount):
        with self.lock:
            if self.cash_available >= amount:
                self.cash_available -= amount
                return True
            return False

    def refill_cash(self, amount):
        with self.lock:
            self.cash_available += amount

# ATM class
class ATM:
    def __init__(self, banking_service, cash_dispenser):
        self.banking_service = banking_service
        self.cash_dispenser = cash_dispenser

    def authenticate_user(self, card, pin):
        account = self.banking_service.get_account(card.card_number)
        if account and card.pin == pin:
            return account
        return None

    def balance_inquiry(self, account):
        return account.get_balance()

    def withdraw_cash(self, account, amount):
        if self.cash_dispenser.dispense_cash(amount) and account.debit(amount):
            return True
        return False

    def deposit_cash(self, account, amount):
        return account.credit(amount)

# ATMDriver to demonstrate usage
if __name__ == "__main__":
    bank = BankingService()
    dispenser = CashDispenser(initial_cash=10000)
    atm = ATM(bank, dispenser)

    # Setup sample accounts
    acc1 = Account("123456", 5000)
    card1 = Card("123456", "1111")
    bank.add_account(acc1)

    # Authenticate
    user_account = atm.authenticate_user(card1, "1111")
    if user_account:
        print("Authenticated successfully!")
        print("Balance:", atm.balance_inquiry(user_account))

        if atm.withdraw_cash(user_account, 1000):
            print("Withdrawal successful.")
        else:
            print("Withdrawal failed.")

        print("Balance after withdrawal:", atm.balance_inquiry(user_account))

        if atm.deposit_cash(user_account, 2000):
            print("Deposit successful.")

        print("Final Balance:", atm.balance_inquiry(user_account))
    else:
        print("Authentication failed.")
