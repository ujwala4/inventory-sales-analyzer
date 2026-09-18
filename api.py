from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from crud import (
    add_sale,
    get_all_sales,
    get_sale,
    update_sale,
    delete_sale,
    search_sales
)

from analysis import (
    calculate_total_sales,
    calculate_total_quantity,
    best_selling_categories,
    slow_moving_categories,
    sales_by_category,
    monthly_sales
)




app = FastAPI(
    title="Inventory & Sales Analyzer API",
    description="REST API for managing sales and analyzing retail data",
    version="1.0.0"
)





class Sale(BaseModel):

    transaction_id: int
    date: str
    customer_id: str
    gender: str
    age: int
    product_category: str
    quantity: int
    price_per_unit: float


class SaleUpdate(BaseModel):

    quantity: int
    price_per_unit: float




@app.get("/")
def home():

    return {
        "message": "Inventory & Sales Analyzer API is running",
        "docs": "/docs"
    }



@app.get("/sales")
def get_sales():

    try:

        df = get_all_sales()

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@app.get("/sales/{transaction_id}")
def get_single_sale(transaction_id: int):

    try:

        df = get_sale(
            transaction_id
        )

        if df.empty:

            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return df.iloc[0].to_dict()

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@app.post("/sales")
def create_sale(sale: Sale):

    try:

        result = add_sale(
            sale.transaction_id,
            sale.date,
            sale.customer_id,
            sale.gender,
            sale.age,
            sale.product_category,
            sale.quantity,
            sale.price_per_unit
        )

        return {
            "message": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )




@app.put("/sales/{transaction_id}")
def update_existing_sale(
    transaction_id: int,
    sale: SaleUpdate
):

    try:

        result = update_sale(
            transaction_id,
            sale.quantity,
            sale.price_per_unit
        )

        if result == "Transaction not found.":

            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return {
            "message": result
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )




@app.delete("/sales/{transaction_id}")
def delete_existing_sale(
    transaction_id: int
):

    try:

        result = delete_sale(
            transaction_id
        )

        if result == "Transaction not found.":

            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return {
            "message": result
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )




@app.get("/sales/search/{search_text}")
def search_existing_sales(
    search_text: str
):

    try:

        df = search_sales(
            search_text
        )

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



@app.get("/analytics/total-sales")
def get_total_sales():

    try:

        total_sales = (
            calculate_total_sales()
        )

        return {
            "total_sales": total_sales
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@app.get("/analytics/total-quantity")
def get_total_quantity():

    try:

        total_quantity = (
            calculate_total_quantity()
        )

        return {
            "total_quantity_sold":
                total_quantity
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/analytics/best-selling")
def get_best_selling():

    try:

        df = best_selling_categories()

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/analytics/slow-moving")
def get_slow_moving():

    try:

        df = slow_moving_categories()

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/analytics/category-sales")
def get_category_sales():

    try:

        df = sales_by_category()

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/analytics/monthly-sales")
def get_monthly_sales():

    try:

        df = monthly_sales()

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@app.get("/analytics/summary")
def get_analytics_summary():

    try:

        total_sales = (
            calculate_total_sales()
        )

        total_quantity = (
            calculate_total_quantity()
        )

        best_selling = (
            best_selling_categories()
        )

        slow_moving = (
            slow_moving_categories()
        )

        category_sales = (
            sales_by_category()
        )

        monthly = (
            monthly_sales()
        )

        return {

            "total_sales":
                total_sales,

            "total_quantity_sold":
                total_quantity,

            "best_selling_categories":
                best_selling.to_dict(
                    orient="records"
                ),

            "slow_moving_categories":
                slow_moving.to_dict(
                    orient="records"
                ),

            "sales_by_category":
                category_sales.to_dict(
                    orient="records"
                ),

            "monthly_sales":
                monthly.to_dict(
                    orient="records"
                )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
import gradio as gr
from app import app as gradio_app

app = gr.mount_gradio_app(
    app,
    gradio_app,
    path="/"
)
