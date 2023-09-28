import pytest
from app.calculations import add,substract,multiply,divide, BankAccount


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1 , num2 , expected" , [(3,2,5), (5,5,10),(12,4,16) ])
def test_add(num1,num2,expected): 
    print("testing add function")
    assert add(num1,num2) == expected


def test_substract():
    assert substract(9,4) == 5


def test_multiply():
    assert multiply(3,4) == 12



def test_divide():
    assert divide(4,2) == 2



def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_account(zero_bank_account):
    assert zero_bank_account.balance == 0



def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40  


def test_deposite(bank_account):
    bank_account.deposite(30)
    assert bank_account.balance == 80      


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,3) == 55          


@pytest.mark.parametrize("deposited , withdrew , expected" , [(200,100,100), (50,40,10),(1200,200,1000)])
def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposite(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_fund(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)