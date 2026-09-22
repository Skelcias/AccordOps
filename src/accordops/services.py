from accordops.db import (
    get_connection,
    get_expense_by_id,
    update_expense_amount,
    delete_expense,
    get_policy_by_id,
    update_policy,
)
import io
from pypdf import PdfReader
from decimal import Decimal
from PIL import Image
import pytesseract


class ExpenseNotFoundError(Exception):
    pass


class PolicyNotFoundError(Exception):
    pass


## méthodes de services


def get_expense_service(item_id: int):
    with get_connection() as conn:
        return _get_expense_or_raise(conn, item_id)


def update_expense_service(item_id: int, new_amount: Decimal):
    with get_connection() as conn:
        expense = _get_expense_or_raise(conn, item_id)
        update_expense_amount(
            conn, item_id, new_amount if new_amount is not None else expense["amount"]
        )
        return get_expense_by_id(conn, item_id)


def delete_expense_service(item_id: int):
    with get_connection() as conn:
        _get_expense_or_raise(conn, item_id)
        delete_expense(conn, item_id)


def get_policy_service(policy_id: int):
    with get_connection() as conn:
        return _get_policy_or_raise(conn, policy_id)


def update_policy_service(
    policy_id: int, new_amount: Decimal | None, new_category: str | None
):
    with get_connection() as conn:
        policy = _get_policy_or_raise(conn, policy_id)
        update_policy(
            conn,
            policy_id,
            new_category if new_category is not None else policy["category"],
            new_amount if new_amount else policy["max_amount"],
        )
        return get_policy_by_id(conn, policy_id)


## helpers


def _get_expense_or_raise(conn, item_id: int):
    expense = get_expense_by_id(conn, item_id)
    if expense is None:
        raise ExpenseNotFoundError
    return expense


def _get_policy_or_raise(conn, policy_id: int):
    policy = get_policy_by_id(conn, policy_id)
    if policy is None:
        raise PolicyNotFoundError
    return policy


def pdf_extraction(content):
    # creation objet python lisible par pyPDF
    file_like_object = io.BytesIO(content)
    reader = PdfReader(file_like_object)
    text_content = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_content.append(page_text)
    return "\n".join(text_content)


def image_extraction(content):
    image = Image.open(io.BytesIO(content))
    texte = pytesseract.image_to_string(image)
    return texte
