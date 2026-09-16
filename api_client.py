import requests


BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# HELPER
# ============================================================

def handle_response(response):

    response.raise_for_status()

    return response.json()


# ============================================================
# SALES APIs
# ============================================================


# ------------------------------------------------------------
# GET ALL SALES
# ------------------------------------------------------------

def get_sales():

    response = requests.get(
        f"{BASE_URL}/sales"
    )

    return handle_response(response)


# ------------------------------------------------------------
# GET ONE SALE
# ------------------------------------------------------------

def get_sale(transaction_id):

    response = requests.get(
        f"{BASE_URL}/sales/{transaction_id}"
    )

    return handle_response(response)


# ------------------------------------------------------------
# ADD SALE
# ------------------------------------------------------------

def create_sale(
    transaction_id,
    date,
    customer_id,
    gender,
    age,
    product_category,
    quantity,
    price_per_unit
):

    data = {

        "transaction_id":
            transaction_id,

        "date":
            date,

        "customer_id":
            customer_id,

        "gender":
            gender,

        "age":
            age,

        "product_category":
            product_category,

        "quantity":
            quantity,

        "price_per_unit":
            price_per_unit
    }

    response = requests.post(
        f"{BASE_URL}/sales",
        json=data
    )

    return handle_response(response)


# ------------------------------------------------------------
# UPDATE SALE
# ------------------------------------------------------------

def update_sale(
    transaction_id,
    quantity,
    price_per_unit
):

    data = {

        "quantity":
            quantity,

        "price_per_unit":
            price_per_unit
    }

    response = requests.put(
        f"{BASE_URL}/sales/{transaction_id}",
        json=data
    )

    return handle_response(response)


# ------------------------------------------------------------
# DELETE SALE
# ------------------------------------------------------------

def delete_sale(transaction_id):

    response = requests.delete(
        f"{BASE_URL}/sales/{transaction_id}"
    )

    return handle_response(response)


# ------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------

def search_sales(search_text):

    response = requests.get(
        f"{BASE_URL}/sales/search/{search_text}"
    )

    return handle_response(response)


# ============================================================
# ANALYTICS APIs
# ============================================================


# ------------------------------------------------------------
# TOTAL SALES
# ------------------------------------------------------------

def get_total_sales():

    response = requests.get(
        f"{BASE_URL}/analytics/total-sales"
    )

    return handle_response(response)


# ------------------------------------------------------------
# TOTAL QUANTITY
# ------------------------------------------------------------

def get_total_quantity():

    response = requests.get(
        f"{BASE_URL}/analytics/total-quantity"
    )

    return handle_response(response)


# ------------------------------------------------------------
# BEST SELLING
# ------------------------------------------------------------

def get_best_selling():

    response = requests.get(
        f"{BASE_URL}/analytics/best-selling"
    )

    return handle_response(response)


# ------------------------------------------------------------
# SLOW MOVING
# ------------------------------------------------------------

def get_slow_moving():

    response = requests.get(
        f"{BASE_URL}/analytics/slow-moving"
    )

    return handle_response(response)


# ------------------------------------------------------------
# CATEGORY SALES
# ------------------------------------------------------------

def get_category_sales():

    response = requests.get(
        f"{BASE_URL}/analytics/category-sales"
    )

    return handle_response(response)


# ------------------------------------------------------------
# MONTHLY SALES
# ------------------------------------------------------------

def get_monthly_sales():

    response = requests.get(
        f"{BASE_URL}/analytics/monthly-sales"
    )

    return handle_response(response)


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

def get_summary():

    response = requests.get(
        f"{BASE_URL}/analytics/summary"
    )

    return handle_response(response)