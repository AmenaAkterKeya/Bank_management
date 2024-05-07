import random
from datetime import datetime

class Bank:
    users = []
    admin = []

    def __init__(self, name):
        self.name = name
        self.balance = 100000
        self.bank_status = False
        self.loan_status = True

    @classmethod
    def find_account(cls, id):
        for account in cls.users:
            if account.account_id == id:
                return account
        return None

    def show_all_users(self):
        print("Name: \t Balance \t Account_id")
        for user in self.users:
            print(f"{user.name} \t\t {user.balance} \t\t {user.account_id}")

    def delete_user(self, id):
        user = self.find_account(id)
        if user:
            self.users.remove(user)
            print("Account deleted successfully.")
        else:
            print("Bank account not found.")

    def show_balance(self):
        print(f"The bank has {self.balance} tk ")

    def total_loans(self):
        total = 0
        for user in self.users:
            total += user.loans
        return total

    def set_loan_status(self, status):
        self.loan_status = status


class Account:
    def __init__(self, name, email, address, account_type, password):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.password = password
        self.balance = 0
        self.account_id = self.generate_account_number(name, email)

    def generate_account_number(self, name, email):
        while True:
            random_number = str(random.randint(1, 100000))
            account_info = name[:4] + random_number[:4] + email[:3]
            if not any(account_info == user.account_id for user in Bank.users):
                return account_info


class User(Account):
    def __init__(self, name, email, address, account_type, password):
        super().__init__(name, email, address, account_type, password)
        self.transection_history = []
        self.loans = 0
        self.loan_time = 0
        Bank.users.append(self)

    def deposit(self, bank, amount, account_id):
        account = bank.find_account(account_id)
        if account:
            if amount > 0:
                account.balance += amount
                bank.balance += amount
                print(f'You successfully deposited {amount}.')
                self.transection_history.append(f"{datetime.now()} \t\t Deposit \t\t {amount}")
            else:
                print('Invalid deposit amount.')
        else:
            print("Account not found.")

    def withdraw(self, bank, amount, account_id):
        account = bank.find_account(account_id)
        if account:
            if account.balance >= amount and amount > 0:
                if bank.bank_status:
                    print("Bank is bankrupt")
                    return
                account.balance -= amount
                bank.balance -= amount
                print(f"Withdrew {amount}.")
                self.transection_history.append(f"{datetime.now()} \t\t withdraw \t\t {amount}")
            else:
                print("Withdrawal amount exceeded.")
        else:
            print("Account not found.")

    def show_available_balance(self, bank, account_id):
        account = bank.find_account(account_id)
        if account:
            print(f"{self.name} your account Balance is {account.balance}")
        else:
            print("Account not found.")

    def check_history(self, account_id):
        account = bank.find_account(account_id)
        if account:
            print("***** Transaction History *****")
            print(f"*** Date ***   \t\t\t   *** Amount ***")
            for history in self.transection_history:
                print(history)
        else:
            print("Account not found.")

    def transfer_money(self, bank, amount, sender_account, recipient_account):
        sender = bank.find_account(sender_account)
        recipient = bank.find_account(recipient_account)
        if sender and recipient:
            if sender.balance >= amount:
                sender.balance -= amount
                recipient.balance += amount
                print(f"{amount} tk successfully transfer to {recipient_account}")
                self.transection_history.append(f"{datetime.now()} \t\t Transfer \t\t {amount}")
            else:
                print("Invalid amount!")
        else:
            print("Account does not exist!")

    def take_loan(self, bank, amount):
        if self.loan_time < 2 and bank.balance >= amount and not bank.bank_status and amount > 0 and bank.loan_status:
            self.loan_time += 1
            bank.balance -= amount
            self.loans += amount
            print(f"Your loan of {amount} tk has been approved!")
        else:
            print("Sorry, your loan request is rejected.")


class Admin(Account):
    def __init__(self, name, email, address, account_type, password):
        super().__init__(name, email, address, account_type, password)
        Bank.admin.append(self)

    def see_all_user_account_list(self, bank):
        bank.show_all_users()

    def delete_user(self, bank, account_id):
        bank.delete_user(account_id)

    def show_bank_balance(self, bank):
        print(f"Total bank balance: {bank.balance} tk")

    def show_total_loans_amount(self, bank):
        total_loans = bank.total_loans()
        print(f"Total amount of loans issued: {total_loans} tk")

    def set_loan_status(self, bank, status):
        bank.set_loan_status(status)


bank = Bank("ABC Bank")

def user_interaction():
    while True:
        print("1. Sign in")
        print("2. Check Balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transaction history")
        print("6. Transfer money")
        print("7. Apply Loan")
        print("8. Sign out")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter your account type: ")
            password = input("Enter your password : ")
            user = User(name=name, email=email, address=address, account_type=account_type, password=password)
            account_id = user.account_id
            print(f"Your Account Id: {account_id}")
        elif choice == "2":
            if user:
                account_id = input("Enter account number: ")
                user.show_available_balance(bank, account_id)
            else:
                print("Please sign in first.")
        elif choice == "3":
            if user:
                account_id = input("Enter account number: ")
                money = int(input("Enter the deposit amount: "))
                user.deposit(bank, money, account_id)
            else:
                print("Please sign in first.")
        elif choice == "4":
            if user:
                account_id = input("Enter account number: ")
                amount = int(input("Enter the amount for Withdraw: "))
                user.withdraw(bank, amount, account_id)
            else:
                print("Please sign in first.")
        elif choice == "5":
            if user:
                account_id = input("Enter account number: ")
                user.check_history(account_id)
            else:
                print("Please sign in first.")
        elif choice == "6":
            if user:
                sender_account = input("Enter your account number: ")
                recipient = input("Enter recipient's account number: ")
                amount = int(input("Enter amount to transfer: "))
                user.transfer_money(bank, amount, sender_account, recipient)
            else:
                print("Please sign in first.")
        elif choice == "7":
            if user:
                amount = int(input("Enter amount to take as loan: "))
                user.take_loan(bank, amount)
            else:
                print("Please sign in first.")
        elif choice == "8":
            break
        else:
            print("Invalid choice !!!")

def admin_interaction():
    while True:
        print("1. Sign in")
        print("2. Show all user accounts")
        print("3. Delete bank account")
        print("4. Total balance of bank")
        print("5. Total amount of loan")
        print("6. Loan feature")
        print("7. Sign out")
        choice = input("Enter your choice: ")
        admin =Admin("A","a@gmail.com","Dhaka","admin",123)
        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter your account type: ")
            password = input("Enter your password : ")
            user = User(name=name, email=email, address=address, account_type=account_type, password=password)
            account_id = user.account_id
            print(f"Your Account Id: {account_id}")
        elif choice == "2":
            if admin:
                admin.see_all_user_account_list(bank)
            else:
                print("Please sign in first.")
        elif choice == "3":
            if admin:
                user_id = input("Enter the user id: ")
                admin.delete_user(bank, user_id)
            else:
                print("Please sign in first.")
        elif choice == "4":
            if admin:
                admin.show_bank_balance(bank)
            else:
                print("Please sign in first.")
        elif choice == "5":
            if admin:
                admin.show_total_loans_amount(bank)
            else:
                print("Please sign in first.")
        elif choice == "6":
            if admin:
                status = input("Enter True or False to enable or disable loan feature: ")
                status = True if status.lower() == "true" else False
                admin.set_loan_status(bank, status)
            else:
                print("Please sign in first.")
        elif choice == "7":
            break
        else:
            print("Invalid choice!")



while True:
    print("Welcome to ABC Bank")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
            user_interaction()
    elif choice == "2":
            admin_interaction()
    elif choice == "3":
        print("Thank you for using ABC Bank!")
        break
    else:
        print("Invalid choice!")

