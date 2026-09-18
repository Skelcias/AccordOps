from accordops.db   import get_connection,add_expense,get_expenses,add_policy,get_policies
from accordops.main import compare_policy_to_expense

def test_add_expense():
    conn = get_connection()

    try:
        add_expense(conn,'restaurant',39.0)
        expenses = get_expenses(conn)

        assert any(
            expense["category"] == "restaurant"
            and expense["amount"] == 39.0
            for expense in expenses
        )
    finally:
        conn.rollback()
        conn.close()

def test_compare():
    conn = get_connection()

    try:
        add_policy(conn,'integration_test',50.0)
        add_expense(conn,'integration_test',70.0)

        policies = get_policies(conn)
        expenses = get_expenses(conn)

        answers = compare_policy_to_expense(policies,expenses)

        assert any(
            answer["category"] == "integration_test"
            and answer["status"] == "non_conforme"
            and answer["difference"] == "20.00"
            for answer in answers
        )
    finally: 
        conn.rollback()
        conn.close()