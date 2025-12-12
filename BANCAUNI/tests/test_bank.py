import os
import tempfile
import pytest

from bank_sim.bank import Bank


def make_bank(tmpdir):
    db_path = os.path.join(tmpdir, "bank_db.json")
    return Bank(db_path)


def test_create_account_and_get(tmpdir):
    b = make_bank(str(tmpdir))
    assert b.create_account("12345678", "Alice", "1234") is True
    c = b.get_client("12345678")
    assert c is not None
    assert c.name == "Alice"
    assert c.balance == 0.0


def test_create_account_invalid_dni(tmpdir):
    b = make_bank(str(tmpdir))
    with pytest.raises(ValueError):
        b.create_account("1234", "Bob", "0000")


def test_deposit_and_withdraw(tmpdir):
    b = make_bank(str(tmpdir))
    b.create_account("11112222", "Carol", "1111")
    b.deposit("11112222", 100.0)
    c = b.get_client("11112222")
    assert c.balance == 100.0
    b.withdraw("11112222", 40.0)
    assert pytest.approx(c.balance, 0.001) == 60.0


def test_withdraw_insufficient(tmpdir):
    b = make_bank(str(tmpdir))
    b.create_account("22223333", "Dave", "2222")
    with pytest.raises(ValueError):
        b.withdraw("22223333", 10.0)


def test_transfer(tmpdir):
    b = make_bank(str(tmpdir))
    b.create_account("33334444", "Eve", "3333")
    b.create_account("44445555", "Frank", "4444")
    b.deposit("33334444", 200.0)
    b.transfer("33334444", "44445555", 75.0)
    a = b.get_client("33334444")
    d = b.get_client("44445555")
    assert pytest.approx(a.balance, 0.001) == 125.0
    assert pytest.approx(d.balance, 0.001) == 75.0
