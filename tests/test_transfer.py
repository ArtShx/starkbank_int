import pytest

from dummy import Dummy

from starkbank_integration.exceptions import InvalidBankAccount, InvalidTaxId
from starkbank_integration.models.bank import BankAccount
from starkbank_integration.transfer import TransferCreateRequest, Transfer


user = Dummy.get_users(1)[0]
bank_acc = Dummy.get_bank_accounts(1)[0]

def test_bank_code_validation():
    sample = [
        ["12345678", True],
        ["123", True],
        [123, False],
        ["1234567", False],
        ["123456789", False],
        ["AAAAAAAA", False],
        ["1234567A", False],
        [12345678, False],
        ["", False],
        ["1", False],
        ["a", False],
        ["A", False],
        [True, False],
        [0, False],
        [None, False],
        [[], False],
        [["a", "b"], False],
        [{}, False]
    ]


    for bank_code, expected in sample:
        assert BankAccount._is_valid_bank_code(bank_code) == expected

def test_branch_code_and_acc_number_validation():
    sample = [
        ["12345678", True],
        ["1234567-8", True],
        ["123-4", True],
        ["1234", True],
        [123, False],
        ["AAAAAAAA", False],
        ["1234567A", False],
        [12345678, False],
        ["", False],
        ["1", True],
        ["a", False],
        ["A", False],
        [True, False],
        [0, False],
        [None, False],
        [[], False],
        [["a", "b"], False],
        [{}, False]
    ]


    for bank_code, expected in sample:
        assert BankAccount._is_valid_branch_code_or_account_number(bank_code) == expected

def test_create_bank_account():
    bank = BankAccount(
            user.name,
            user.user_type,
            user.tax_id, 
            bank_acc.bank_code, 
            bank_acc.branch_code, 
            bank_acc.account_number)

    # properties should be accessible
    assert bank.name == user.name
    assert bank.user_type == user.user_type
    assert bank.tax_id == user.tax_id
    assert bank.bank_code == bank_acc.bank_code
    assert bank.branch_code == bank_acc.branch_code
    assert bank.account_number == bank_acc.account_number

    with pytest.raises(InvalidBankAccount):
        BankAccount(
            user.name,
            user.user_type,
            user.tax_id, 
            "Invalid", 
            bank_acc.branch_code, 
            bank_acc.account_number)
    
    with pytest.raises(InvalidTaxId):
        BankAccount(
            user.name,
            user.user_type,
            "Invalid", 
            bank_acc.bank_code, 
            bank_acc.branch_code, 
            bank_acc.account_number)

def test_transfer_create():
    transfer_req = TransferCreateRequest(
        user.name,
        user.user_type,
        user.tax_id, 
        10,
        bank_acc.bank_code, 
        bank_acc.branch_code, 
        bank_acc.account_number)
    Transfer.create(transfer_req)
