import csv
from datetime import datetime
import pandas as pd
import numpy as np

# ------------------ Account Class ------------------
class Account:
    def __init__(self, acc_no, name, acc_type, balance, status="Active", created_date=None):
        self.acc_no = acc_no
        self.name = name
        self.acc_type = acc_type
        self.balance = float(balance)
        self.status = status
        self.created_date = created_date if created_date else datetime.now().strftime("%Y-%m-%d")


# ------------------ Banking System ------------------
class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    # ------------------ Load Accounts ------------------
    def load_accounts(self):
        try:
            with open("accounts.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    acc = Account(*row)
                    self.accounts[row[0]] = acc
        except:
            pass

    # ------------------ Save Accounts ------------------
    def save_accounts(self):
        with open("accounts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for acc in self.accounts.values():
                writer.writerow([
                    acc.acc_no,
                    acc.name,
                    acc.acc_type,
                    acc.balance,
                    acc.status,
                    acc.created_date
                ])

    # ------------------ Create Account ------------------
    def create_account(self):
        acc_no = input("Enter Account Number: ")
        name = input("Enter Name: ")
        acc_type = input("Enter Type (Savings/Current): ")
        balance = float(input("Enter Balance: "))

        self.accounts[acc_no] = Account(acc_no, name, acc_type, balance)
        self.save_accounts()
        print("Account Created")

    # ------------------ Deposit ------------------
    def deposit(self):
        acc_no = input("Account Number: ")
        amount = float(input("Amount: "))

        if acc_no in self.accounts:
            self.accounts[acc_no].balance += amount
            self.log_transaction(acc_no, "Deposit", amount)
            self.save_accounts()
            print("Deposit Done")
        else:
            print("Account Not Found")

    # ------------------ Withdraw ------------------
    def withdraw(self):
        acc_no = input("Account Number: ")
        amount = float(input("Amount: "))

        if acc_no in self.accounts:
            if self.accounts[acc_no].balance >= amount:
                self.accounts[acc_no].balance -= amount
                self.log_transaction(acc_no, "Withdraw", amount)
                self.save_accounts()
                print("Withdraw Done")
            else:
                print("Insufficient Balance")
        else:
            print("Account Not Found")

    # ------------------ Transfer ------------------
    def transfer(self):
        sender = input("Sender Account: ")
        receiver = input("Receiver Account: ")
        amount = float(input("Amount: "))

        if sender in self.accounts and receiver in self.accounts:
            if self.accounts[sender].balance >= amount:
                self.accounts[sender].balance -= amount
                self.accounts[receiver].balance += amount

                self.log_transaction(sender, "Transfer Out", amount)
                self.log_transaction(receiver, "Transfer In", amount)

                self.save_accounts()
                print("Transfer Successful")
            else:
                print("Insufficient Balance")
        else:
            print("Invalid Accounts")

    # ------------------ View ------------------
    def view_accounts(self):
        for acc in self.accounts.values():
            print(acc.acc_no, acc.name, acc.acc_type, acc.balance, acc.status)

    # ------------------ Search ------------------
    def search(self):
        key = input("Enter Account Number/Name: ")
        for acc in self.accounts.values():
            if acc.acc_no == key or acc.name.lower() == key.lower():
                print(acc.acc_no, acc.name, acc.acc_type, acc.balance, acc.status)

    # ------------------ Analytics ------------------
    def analytics(self):
        if not self.accounts:
            print("No Data Available")
            return

        data = []
        for acc in self.accounts.values():
            data.append([acc.acc_no, acc.name, acc.acc_type, acc.balance])

        df = pd.DataFrame(data, columns=["AccNo", "Name", "Type", "Balance"])
        balances = df["Balance"].values

        print("\nFinancial Analytics")
        print("Total Bank Balance:", np.sum(balances))
        print("Average Balance:", np.mean(balances))

        max_acc = df.loc[df["Balance"].idxmax()]
        min_acc = df.loc[df["Balance"].idxmin()]

        print("Highest Balance:", max_acc["Name"], max_acc["Balance"])
        print("Lowest Balance:", min_acc["Name"], min_acc["Balance"])

        print("\nAccount Type Distribution:")
        print(df["Type"].value_counts())

    # ------------------ Insights ------------------
    def insights(self):
        print("\nInsights")

        for acc in self.accounts.values():
            if acc.balance < 1000:
                print(f"Low Balance Alert: {acc.name} ({acc.balance})")

            if acc.status == "Active":
                created = datetime.strptime(acc.created_date, "%Y-%m-%d")
                if (datetime.now() - created).days > 365:
                    print(f"Old Account: {acc.name}")

    # ------------------ Transaction Log ------------------
    def log_transaction(self, acc_no, t_type, amount):
        with open("transactions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([acc_no, t_type, amount, datetime.now()])

    # ------------------ Transaction History ------------------
    def transaction_history(self):
        acc_no = input("Enter Account Number: ")
        try:
            df = pd.read_csv("transactions.csv", header=None)
            df.columns = ["AccNo", "Type", "Amount", "Date"]
            print(df[df["AccNo"] == acc_no])
        except:
            print("No Transactions Found")


# ------------------ Main ------------------
def main():
    bank = BankSystem()

    while True:
        print("\n--- SMART BANKING SYSTEM ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View Accounts")
        print("6. Search")
        print("7. Analytics")
        print("8. Insights")
        print("9. Transaction History")
        print("10. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            bank.create_account()
        elif choice == "2":
            bank.deposit()
        elif choice == "3":
            bank.withdraw()
        elif choice == "4":
            bank.transfer()
        elif choice == "5":
            bank.view_accounts()
        elif choice == "6":
            bank.search()
        elif choice == "7":
            bank.analytics()
        elif choice == "8":
            bank.insights()
        elif choice == "9":
            bank.transaction_history()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()