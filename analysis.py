import sqlite3
import pandas as pd


DB_NAME = "inventory.db"


# ============================================================
# GET SALES DATA
# ============================================================

def get_sales_data():

    conn = sqlite3.connect(DB_NAME)

    try:
        df = pd.read_sql_query(
            "SELECT * FROM sales",
            conn
        )

        return df

    finally:
        conn.close()


# ============================================================
# TOTAL SALES
# ============================================================

def calculate_total_sales():

    df = get_sales_data()

    if df.empty:
        return 0

    return float(
        df["total_amount"].sum()
    )


# ============================================================
# TOTAL QUANTITY
# ============================================================

def calculate_total_quantity():

    df = get_sales_data()

    if df.empty:
        return 0

    return int(
        df["quantity"].sum()
    )


# ============================================================
# BEST SELLING CATEGORIES
# ============================================================

def best_selling_categories():

    df = get_sales_data()

    if df.empty:
        return pd.DataFrame(
            columns=[
                "Category",
                "Quantity Sold"
            ]
        )

    result = (
        df.groupby("product_category")["quantity"]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    result.columns = [
        "Category",
        "Quantity Sold"
    ]

    return result


# ============================================================
# SLOW MOVING CATEGORIES
# ============================================================

def slow_moving_categories():

    df = get_sales_data()

    if df.empty:
        return pd.DataFrame(
            columns=[
                "Category",
                "Quantity Sold"
            ]
        )

    category_sales = (
        df.groupby("product_category")["quantity"]
        .sum()
        .reset_index()
    )

    average_quantity = (
        category_sales["quantity"].mean()
    )

    slow_moving = category_sales[
        category_sales["quantity"]
        < average_quantity
    ].copy()

    slow_moving = slow_moving.sort_values(
        "quantity"
    )

    slow_moving.columns = [
        "Category",
        "Quantity Sold"
    ]

    return slow_moving


# ============================================================
# SALES BY CATEGORY
# ============================================================

def sales_by_category():

    df = get_sales_data()

    if df.empty:
        return pd.DataFrame(
            columns=[
                "Category",
                "Total Sales"
            ]
        )

    result = (
        df.groupby("product_category")["total_amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    result.columns = [
        "Category",
        "Total Sales"
    ]

    return result


# ============================================================
# MONTHLY SALES
# ============================================================

def monthly_sales():

    df = get_sales_data()

    if df.empty:
        return pd.DataFrame(
            columns=[
                "Month",
                "Total Sales"
            ]
        )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    result = (
        df.groupby(
            df["date"].dt.to_period("M")
        )["total_amount"]
        .sum()
        .reset_index()
    )

    result["date"] = (
        result["date"]
        .astype(str)
    )

    result.columns = [
        "Month",
        "Total Sales"
    ]

    return result


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    print(
        "Total Sales:",
        calculate_total_sales()
    )

    print(
        "Total Quantity:",
        calculate_total_quantity()
    )

    print(
        "\nBest Selling Categories:"
    )

    print(
        best_selling_categories()
    )

    print(
        "\nSlow Moving Categories:"
    )

    print(
        slow_moving_categories()
    )

    print(
        "\nSales By Category:"
    )

    print(
        sales_by_category()
    )

    print(
        "\nMonthly Sales:"
    )

    print(
        monthly_sales()
    )