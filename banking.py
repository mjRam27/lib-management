account_number = "de123"
owner = "srh"
balance = 1000


def deposite(balance, amount):
    return balance + amount


def withdraw(balance, amount):
    return balance - amount


print("starting balance:", balance)

balance = deposite(balance, 500)
print("balance after deposite:", balance)

balance = withdraw(balance, 200)
print("balance after withdraw:", balance)
