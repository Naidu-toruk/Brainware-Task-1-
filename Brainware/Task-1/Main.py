import getpass
from datetime import datetime
import time

class BankAccount:
    def __init__(self, user_id, pin, name, balance):
        self.user_id = user_id
        self.pin = pin
        self.name = name
        self.balance = balance
        self.transaction_history = []
        self.currency_rates = {'USD': 1.0, 'EUR': 0.85, 'GBP': 0.75, 'INDIANRS' : 86}

    def record_transaction(self, type_, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append({
            'timestamp': timestamp,
            'type': type_,
            'amount': amount,
            'balance': self.balance
        })

    def convert_currency(self, target_currency):
        rate = self.currency_rates.get(target_currency.upper(), None)
        if rate:
            return self.balance * rate
        return None

# Sample accounts
accounts = [
    BankAccount('ACCT1001', '7890', 'Alice Johnson', 1500.00),
    BankAccount('ACCT2002', '4321', 'Bob Smith', 3000.50)
]

def authenticate_user():
    """Enhanced authentication with attempt tracking"""
    attempts = 0
    while attempts < 3:
        user_id = input("\nEnter Account ID: ").strip()
        account = next((acc for acc in accounts if acc.user_id == user_id), None)
        
        if not account:
            print("❌ Account not found. Please try again.")
            attempts += 1
            continue
            
        pin = getpass.getpass("Enter PIN: ")
        if pin == account.pin:
            print(f"\n🌟 Welcome back, {account.name}!")
            return account
        else:
            print("⚠️ Incorrect PIN. Please try again.")
            attempts += 1
            
    print("\n🔒 Account locked. Too many failed attempts.")
    return None

def display_main_menu():
    """Enhanced menu with new features"""
    print("\n════════════ MAIN MENU ════════════")
    print("1. View Account Balance")
    print("2. Deposit Money")
    print("3. Withdraw Cash")
    print("4. Transaction History")
    print("5. Currency Converter")
    print("6. Exit")
    print("═══════════════════════════════════")

def get_numeric_input(prompt):
    """Safe numeric input handling"""
    while True:
        try:
            value = float(input(prompt))
            return round(value, 2)
        except ValueError:
            print("⚠️ Invalid input. Please enter numbers only.")

def handle_deposit(account):
    """Enhanced deposit handling"""
    amount = get_numeric_input("\nEnter deposit amount: $")
    if amount <= 0:
        print("⚠️ Deposit amount must be positive.")
        return
    
    account.balance += amount
    account.record_transaction('DEPOSIT', amount)
    print(f"\n✅ Success! New balance: ${account.balance:.2f}")

def handle_withdrawal(account):
    """Enhanced withdrawal with multiple checks"""
    amount = get_numeric_input("\nEnter withdrawal amount: $")
    
    if amount <= 0:
        print("⚠️ Withdrawal amount must be positive.")
    elif amount > account.balance:
        print("⚠️ Insufficient funds. Transaction canceled.")
    else:
        account.balance -= amount
        account.record_transaction('WITHDRAWAL', -amount)
        print(f"\n✅ Success! Remaining balance: ${account.balance:.2f}")

def show_transaction_history(account):
    """New feature: Transaction history"""
    print("\n══════════ TRANSACTION HISTORY ══════════")
    if not account.transaction_history:
        print("No transactions yet")
    for transaction in account.transaction_history[-5:]:  # Show last 5 transactions
        print(f"{transaction['timestamp']} | {transaction['type']:9} | ${transaction['amount']:7.2f} | Balance: ${transaction['balance']:.2f}")
    print("══════════════════════════════════════════")

def handle_currency_conversion(account):
    """New feature: Currency conversion"""
    print("\nAvailable currencies: USD, EUR, GBP, INDIANRS")
    currency = input("Enter target currency: ").upper()
    converted = account.convert_currency(currency)
    
    if converted is not None:
        print(f"\n💱 Converted balance: {currency} {converted:.2f}")
    else:
        print("⚠️ Invalid currency code. Supported: USD, EUR, GBP, INDIANRS")

def atm_system():
    """Main system with session timeout"""
    print("\n═══════════════ NEXTGEN ATM ═══════════════")
    account = authenticate_user()
    if not account:
        return
        
    last_activity = time.time()
    
    while True:
        if time.time() - last_activity > 120:  # 2-minute timeout
            print("\n🕒 Session timed out due to inactivity")
            return
            
        display_main_menu()
        choice = input("\nEnter option (1-6): ").strip()
        last_activity = time.time()
        
        if choice == '1':
            print(f"\nCurrent Balance: ${account.balance:.2f}")
            
        elif choice == '2':
            handle_deposit(account)
            
        elif choice == '3':
            handle_withdrawal(account)
            
        elif choice == '4':
            show_transaction_history(account)
            
        elif choice == '5':
            handle_currency_conversion(account)
            
        elif choice == '6':
            print("\n💼 Thank you for banking with us. Goodbye!")
            break
            
        else:
            print("⚠️ Invalid choice. Please select 1-6")

if __name__ == "__main__":
    atm_system()