import gradio as gr
import pandas as pd

from api_client import (
    get_sales,
    create_sale,
    update_sale,
    delete_sale,
    search_sales,
    get_summary
)


# ============================================================
# HELPER
# ============================================================

def dataframe_from_json(data):

    return pd.DataFrame(data)


# ============================================================
# DASHBOARD
# ============================================================

def refresh_dashboard():

    try:

        data = get_summary()

        total_sales = data[
            "total_sales"
        ]

        total_quantity = data[
            "total_quantity_sold"
        ]

        best_selling = dataframe_from_json(
            data[
                "best_selling_categories"
            ]
        )

        slow_moving = dataframe_from_json(
            data[
                "slow_moving_categories"
            ]
        )

        category_sales = dataframe_from_json(
            data[
                "sales_by_category"
            ]
        )

        monthly_sales = dataframe_from_json(
            data[
                "monthly_sales"
            ]
        )

        return (
            f"₹{total_sales:,.2f}",
            f"{total_quantity:,}",
            best_selling,
            slow_moving,
            category_sales,
            monthly_sales
        )

    except Exception as e:

        error_df = pd.DataFrame({
            "Error": [str(e)]
        })

        return (
            "Error",
            "Error",
            error_df,
            error_df,
            error_df,
            error_df
        )


# ============================================================
# ADD SALE
# ============================================================

def add_sale_ui(
    transaction_id,
    date,
    customer_id,
    gender,
    age,
    product_category,
    quantity,
    price_per_unit
):

    try:

        result = create_sale(
            int(transaction_id),
            date,
            customer_id,
            gender,
            int(age),
            product_category,
            int(quantity),
            float(price_per_unit)
        )

        return result["message"]

    except Exception as e:

        return f"Error: {e}"


# ============================================================
# READ SALES
# ============================================================

def get_sales_ui():

    try:

        data = get_sales()

        return pd.DataFrame(data)

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })


# ============================================================
# UPDATE SALE
# ============================================================

def update_sale_ui(
    transaction_id,
    quantity,
    price_per_unit
):

    try:

        result = update_sale(
            int(transaction_id),
            int(quantity),
            float(price_per_unit)
        )

        return result["message"]

    except Exception as e:

        return f"Error: {e}"


# ============================================================
# DELETE SALE
# ============================================================

def delete_sale_ui(transaction_id):

    try:

        result = delete_sale(
            int(transaction_id)
        )

        return result["message"]

    except Exception as e:

        return f"Error: {e}"


# ============================================================
# SEARCH SALES
# ============================================================

def search_sales_ui(search_text):

    try:

        if not search_text:

            return get_sales_ui()

        data = search_sales(
            search_text
        )

        return pd.DataFrame(data)

    except Exception as e:

        return pd.DataFrame({
            "Error": [str(e)]
        })


# ============================================================
# GRADIO APPLICATION
# ============================================================

with gr.Blocks(
    title="Inventory & Sales Analyzer"
) as app:

    gr.Markdown(
        """
        # 🛒 Inventory & Sales Analyzer

        Manage retail sales, perform CRUD operations,
        search transactions and analyze sales performance.
        """
    )


    # ========================================================
    # DASHBOARD TAB
    # ========================================================

    with gr.Tab("📊 Dashboard"):

        gr.Markdown(
            "## Sales Overview"
        )

        with gr.Row():

            total_sales_display = gr.Textbox(
                label="Total Sales",
                interactive=False
            )

            total_quantity_display = gr.Textbox(
                label="Total Quantity Sold",
                interactive=False
            )


        gr.Markdown(
            "### Best-Selling Categories"
        )

        best_selling_table = gr.Dataframe(
            interactive=False
        )


        gr.Markdown(
            "### Slow-Moving Categories"
        )

        slow_moving_table = gr.Dataframe(
            interactive=False
        )


        gr.Markdown(
            "### Sales by Category"
        )

        category_sales_table = gr.Dataframe(
            interactive=False
        )


        gr.Markdown(
            "### Monthly Sales"
        )

        monthly_sales_table = gr.Dataframe(
            interactive=False
        )


        refresh_dashboard_button = gr.Button(
            "🔄 Refresh Dashboard"
        )


        refresh_dashboard_button.click(
            fn=refresh_dashboard,
            outputs=[
                total_sales_display,
                total_quantity_display,
                best_selling_table,
                slow_moving_table,
                category_sales_table,
                monthly_sales_table
            ]
        )


    # ========================================================
    # SALES TAB
    # ========================================================

    with gr.Tab("🛍️ Sales"):

        # ----------------------------------------------------
        # ADD SALE
        # ----------------------------------------------------

        gr.Markdown(
            "## Add New Sale"
        )

        with gr.Row():

            add_transaction_id = gr.Number(
                label="Transaction ID"
            )

            add_date = gr.Textbox(
                label="Date",
                placeholder="YYYY-MM-DD"
            )

            add_customer_id = gr.Textbox(
                label="Customer ID"
            )


        with gr.Row():

            add_gender = gr.Dropdown(
                choices=[
                    "Male",
                    "Female"
                ],
                label="Gender"
            )

            add_age = gr.Number(
                label="Age"
            )

            add_category = gr.Dropdown(
                choices=[
                    "Beauty",
                    "Clothing",
                    "Electronics"
                ],
                label="Product Category"
            )


        with gr.Row():

            add_quantity = gr.Number(
                label="Quantity"
            )

            add_price = gr.Number(
                label="Price Per Unit"
            )


        add_button = gr.Button(
            "➕ Add Sale"
        )

        add_result = gr.Textbox(
            label="Result"
        )


        add_button.click(
            fn=add_sale_ui,
            inputs=[
                add_transaction_id,
                add_date,
                add_customer_id,
                add_gender,
                add_age,
                add_category,
                add_quantity,
                add_price
            ],
            outputs=add_result
        )


        # ----------------------------------------------------
        # VIEW SALES
        # ----------------------------------------------------

        gr.Markdown(
            "## All Sales"
        )

        refresh_sales_button = gr.Button(
            "🔄 Refresh Sales"
        )

        sales_table = gr.Dataframe(
            interactive=False
        )


        refresh_sales_button.click(
            fn=get_sales_ui,
            outputs=sales_table
        )


        # ----------------------------------------------------
        # UPDATE SALE
        # ----------------------------------------------------

        gr.Markdown(
            "## Update Sale"
        )

        with gr.Row():

            update_transaction_id = gr.Number(
                label="Transaction ID"
            )

            update_quantity = gr.Number(
                label="New Quantity"
            )

            update_price = gr.Number(
                label="New Price Per Unit"
            )


        update_button = gr.Button(
            "✏️ Update Sale"
        )

        update_result = gr.Textbox(
            label="Result"
        )


        update_button.click(
            fn=update_sale_ui,
            inputs=[
                update_transaction_id,
                update_quantity,
                update_price
            ],
            outputs=update_result
        )


        # ----------------------------------------------------
        # DELETE SALE
        # ----------------------------------------------------

        gr.Markdown(
            "## Delete Sale"
        )

        delete_transaction_id = gr.Number(
            label="Transaction ID"
        )

        delete_button = gr.Button(
            "🗑️ Delete Sale"
        )

        delete_result = gr.Textbox(
            label="Result"
        )


        delete_button.click(
            fn=delete_sale_ui,
            inputs=[
                delete_transaction_id
            ],
            outputs=delete_result
        )


    # ========================================================
    # SEARCH TAB
    # ========================================================

    with gr.Tab("🔎 Search"):

        gr.Markdown(
            """
            ## Search Sales

            Search using transaction ID,
            customer ID, category or gender.
            """
        )


        search_input = gr.Textbox(
            label="Search",
            placeholder="Example: CUST001, Beauty, Male or 10"
        )


        search_button = gr.Button(
            "🔎 Search"
        )


        search_results = gr.Dataframe(
            interactive=False
        )


        search_button.click(
            fn=search_sales_ui,
            inputs=search_input,
            outputs=search_results
        )


# ============================================================
# LAUNCH
# ============================================================
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860
    )