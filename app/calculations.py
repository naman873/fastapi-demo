
def add(a,b):
    return a+b


def substract(a,b):
    return a-b


def multiply(a,b):
    return a*b


def divide(a,b):
    return a/b


class InsufficientFund(Exception):
    pass

class BankAccount():

    def __init__(self,starting_balance=0):
        self.balance =  starting_balance

    def deposite(self,amount):
        self.balance += amount

    def withdraw(self,amount):
        if amount > self.balance:
            raise InsufficientFund("Insufficient money")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
