from accordops.main import compare_with_policy, compare_policy_to_expense

def test_expense_is_compliant():
    result = compare_with_policy(35,20)

    assert result == "Conforme"


def test_expense_is_not_compliant():
    result = compare_with_policy(35, 47.8)

    assert result == "Non conforme de 12.80 $"

def test_expense_is_maximum():
    result = compare_with_policy(35,35)

    assert result == "Conforme"

# ------------------------------------------------- #

def test_missing_category():
    expenses = [{'id': '1', 'category': 'restaurant', 'amount': '47.80'}, {'id': '2', 'category': 'hotel', 'amount': '162.00'}, {'id': '3', 'category': 'taxi', 'amount': '38.00'}, {'id': '4', 'category': 'restaurant', 'amount': '25.00'}]
    policy =  [{'category': 'restaurant', 'max_amount': '35.00'}, {'category': 'hotel', 'max_amount': '180.00'}]

    answers = compare_policy_to_expense(policy=policy,expenses=expenses)

    assert len(answers) == 3

def test_invalid_value():
    expenses = [{'id': '1', 'category': 'restaurant', 'amount': 'abc'}, {'id': '2', 'category': 'hotel', 'amount': '162.00'}, {'id': '3', 'category': 'taxi', 'amount': '38.00'}, {'id': '4', 'category': 'restaurant', 'amount': '25.00'}]
    policy =  [{'category': 'restaurant', 'max_amount': '35.00'}, {'category': 'hotel', 'max_amount': '180.00'}, {'category': 'taxi', 'max_amount': '50.00'}]

    answers = compare_policy_to_expense(policy=policy,expenses=expenses)

    assert len(answers) == 3