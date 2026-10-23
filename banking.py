# account_number = "de123"
# owner = "srh"
# balance = 1000


# def deposite(balance, amount):
#     return balance + amount


# def withdraw(balance, amount):
#     return balance - amount


# print("starting balance:", balance)

# balance = deposite(balance, 500)
# print("balance after deposite:", balance)

# balance = withdraw(balance, 200)
# print("balance after withdraw:", balance)


class BankAccount:
    def __init__(self, account_number, owner, balance):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance

    def deposite(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.balance = self.balance - amount
            return True

account1 = BankAccount("de123", "srh", 1000)
account2 = BankAccount("de456", "abc", 500)

account1.deposite(500)
success = account1.withdraw(200)

print("Account 1 balance:", account1.balance)