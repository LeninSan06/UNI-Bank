import sys
import traceback
from bank_sim.bank import Bank
import os


def make_bank(tmpdir):
    db_path = os.path.join(tmpdir, "bank_db.json")
    # Ensure a clean DB for each test run
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass
    return Bank(db_path)


def run():
    tmpdir = os.path.join(os.path.dirname(__file__), "tmp")
    os.makedirs(tmpdir, exist_ok=True)
    passed = 0
    failed = 0

    tests = []

    def t_create_account_and_get():
        b = make_bank(tmpdir)
        assert b.create_account("12345678", "Alice", "1234") is True
        c = b.get_client("12345678")
        assert c is not None
        assert c.name == "Alice"
        assert c.balance == 0.0

    def t_create_account_invalid_dni():
        b = make_bank(tmpdir)
        try:
            b.create_account("1234", "Bob", "0000")
            raise AssertionError("Expected ValueError")
        except ValueError:
            pass

    def t_deposit_and_withdraw():
        b = make_bank(tmpdir)
        b.create_account("11112222", "Carol", "1111")
        b.deposit("11112222", 100.0)
        c = b.get_client("11112222")
        assert c.balance == 100.0
        b.withdraw("11112222", 40.0)
        assert abs(c.balance - 60.0) < 1e-6

    def t_withdraw_insufficient():
        b = make_bank(tmpdir)
        b.create_account("22223333", "Dave", "2222")
        try:
            b.withdraw("22223333", 10.0)
            raise AssertionError("Expected ValueError")
        except ValueError:
            pass

    def t_transfer():
        b = make_bank(tmpdir)
        b.create_account("33334444", "Eve", "3333")
        b.create_account("44445555", "Frank", "4444")
        b.deposit("33334444", 200.0)
        b.transfer("33334444", "44445555", 75.0)
        a = b.get_client("33334444")
        d = b.get_client("44445555")
        assert abs(a.balance - 125.0) < 1e-6
        assert abs(d.balance - 75.0) < 1e-6

    tests.extend([
        ("create_account_and_get", t_create_account_and_get),
        ("create_account_invalid_dni", t_create_account_invalid_dni),
        ("deposit_and_withdraw", t_deposit_and_withdraw),
        ("withdraw_insufficient", t_withdraw_insufficient),
        ("transfer", t_transfer),
    ])

    for name, fn in tests:
        try:
            fn()
            print(f"[PASS] {name}")
            passed += 1
        except Exception:
            print(f"[FAIL] {name}")
            traceback.print_exc()
            failed += 1

    print("\nSummary:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    if failed > 0:
        sys.exit(2)


if __name__ == '__main__':
    run()
