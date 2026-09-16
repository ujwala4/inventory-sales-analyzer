import sqlite3
import pandas as pd


DB_NAME = "inventory.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ============================================================
# READ - GET ALL SALES
# ============================================================

def get_all_sales():
    conn = get_connection()

    try:
        df = pd.read_sql_query(
            "SELECT * FROM sales",
            conn
        )
        return df
    finally:
        conn.close()


# ============================================================
# READ - GET ONE SALE
# ============================================================

def get_sale(transaction_id):
    conn = get_connection()

    try:
        query = """
        SELECT *
        FROM sales
        WHERE transaction_id = ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(transaction_id,)
        )

        return df
    finally:
        conn.close()


# ============================================================
# CREATE - ADD SALE
# ============================================================

def add_sale(
    transaction_id,
    date,
    customer_id,
    gender,
    age,
    product_category,
    quantity,
    price_per_unit
):
    total_amount = quantity * price_per_unit

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO sales
        (
            transaction_id,
            date,
            customer_id,
            gender,
            age,
            product_category,
            quantity,
            price_per_unit,
            total_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                transaction_id,
                date,
                customer_id,
                gender,
                age,
                product_category,
                quantity,
                price_per_unit,
                total_amount
            )
        )

        conn.commit()

        return "Sale added successfully!"

    finally:
        conn.close()


# ============================================================
# UPDATE - UPDATE SALE
# ============================================================

def update_sale(
    transaction_id,
    quantity,
    price_per_unit
):
    total_amount = quantity * price_per_unit

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        UPDATE sales
        SET
            quantity = ?,
            price_per_unit = ?,
            total_amount = ?
        WHERE transaction_id = ?
        """

        cursor.execute(
            query,
            (
                quantity,
                price_per_unit,
                total_amount,
                transaction_id
            )
        )

        conn.commit()

        if cursor.rowcount == 0:
            return "Transaction not found."

        return "Sale updated successfully!"

    finally:
        conn.close()


# ============================================================
# DELETE - DELETE SALE
# ============================================================

def delete_sale(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        DELETE FROM sales
        WHERE transaction_id = ?
        """

        cursor.execute(
            query,
            (transaction_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return "Transaction not found."

        return "Sale deleted successfully!"

    finally:
        conn.close()


# ============================================================
# SEARCH
# ============================================================

def search_sales(search_text):

    conn = get_connection()

    try:
        query = """
        SELECT *
        FROM sales
        WHERE
            CAST(transaction_id AS TEXT) LIKE ?
            OR customer_id LIKE ?
            OR product_category LIKE ?
            OR gender LIKE ?
        """

        search_term = f"%{search_text}%"

        df = pd.read_sql_query(
            query,
            conn,
            params=(
                search_term,
                search_term,
                search_term,
                search_term
            )
        )

        return df

    finally:
        conn.close()