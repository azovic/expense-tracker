import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database import (
    create_tables,
    add_category,
    add_payment_method,
    get_categories,
    get_payment_methods,
    add_expense,
    list_expenses,
    get_total_expenses,
    get_expenses_by_category,
    get_expenses_by_payment_method,
    delete_expense,
    expense_exists
)
st.markdown(
    """
    <style>
    .stMetric {
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")

create_tables()

st.title("💸 Personal Expense Tracker")
st.write("A simple SQL-based personal finance tracker built with Python, SQLite, and Streamlit.")


menu = st.sidebar.selectbox(
    "Choose a section",
    [
        "Dashboard",
        "Add Category",
        "Add Payment Method",
        "Add Expense",
        "List Expenses",
        "Delete Expense",
        "Reports"
    ]
)


if menu == "Dashboard":
    st.subheader("Dashboard")

    total_expense = get_total_expenses()
    st.metric("Total Expenses", f"{total_expense:.2f} TL")

    category_data = get_expenses_by_category()
if category_data:
    top_category = max(category_data, key=lambda x: x[1])
    st.info(f"Top Category: {top_category[0]} ({top_category[1]:.2f} TL)")


    col1, col2 = st.columns(2)

    with col1:
        st.write("### Expenses by Category")
        category_data = get_expenses_by_category()

        categories = [row[0] for row in category_data if row[1] > 0]
        category_amounts = [row[1] for row in category_data if row[1] > 0]

        if category_amounts:
            fig, ax = plt.subplots()
            ax.bar(categories, category_amounts)
            ax.set_title("Expenses by Category")
            ax.set_xlabel("Category")
            ax.set_ylabel("Amount (TL)")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("No category expense data yet.")

    with col2:
        st.write("### Expense Distribution")
        pie_data = get_expenses_by_category()

        pie_categories = [row[0] for row in pie_data if row[1] > 0]
        pie_amounts = [row[1] for row in pie_data if row[1] > 0]

        if pie_amounts:
            fig, ax = plt.subplots()
            ax.pie(pie_amounts, labels=pie_categories, autopct="%1.1f%%")
            ax.set_title("Expense Distribution by Category")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("No pie chart data yet.")


elif menu == "Add Category":
    st.subheader("Add Category")

    category_name = st.text_input("Category Name")

    if st.button("Add Category"):
        if category_name.strip():
            try:
                add_category(category_name.strip())
                st.success("Category added successfully.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a category name.")


elif menu == "Add Payment Method":
    st.subheader("Add Payment Method")

    payment_name = st.text_input("Payment Method Name")

    if st.button("Add Payment Method"):
        if payment_name.strip():
            try:
                add_payment_method(payment_name.strip())
                st.success("Payment method added successfully.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a payment method name.")


elif menu == "Add Expense":
    st.subheader("Add Expense")

    categories = get_categories()
    payment_methods = get_payment_methods()

    if not categories:
        st.warning("Please add a category first.")
    elif not payment_methods:
        st.warning("Please add a payment method first.")
    else:
        category_dict = {category_name: category_id for category_id, category_name in categories}
        payment_dict = {payment_name: payment_id for payment_id, payment_name in payment_methods}

        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        expense_date = st.date_input("Expense Date")
        description = st.text_input("Description")
        selected_category = st.selectbox("Category", list(category_dict.keys()))
        selected_payment = st.selectbox("Payment Method", list(payment_dict.keys()))

        if st.button("Add Expense"):
            add_expense(
                amount=float(amount),
                expense_date=str(expense_date),
                description=description.strip(),
                category_id=category_dict[selected_category],
                payment_id=payment_dict[selected_payment]
            )
            st.success("Expense added successfully.")


elif menu == "List Expenses":
    st.subheader("List Expenses")

    expenses = list_expenses()

    if expenses:
        df = pd.DataFrame(
            expenses,
            columns=["Expense ID", "Amount", "Date", "Description", "Category", "Payment Method"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No expenses found.")


elif menu == "Delete Expense":
    st.subheader("Delete Expense")

    expenses = list_expenses()

    if expenses:
        df = pd.DataFrame(
            expenses,
            columns=["Expense ID", "Amount", "Date", "Description", "Category", "Payment Method"]
        )
        st.dataframe(df, use_container_width=True)

        expense_id = st.number_input("Enter Expense ID to delete", min_value=1, step=1)

        if st.button("Delete Expense"):
            if expense_exists(int(expense_id)):
                delete_expense(int(expense_id))
                st.success("Expense deleted successfully.")
            else:
                st.error("Expense ID not found.")
    else:
        st.info("No expenses available to delete.")


elif menu == "Reports":
    st.subheader("Reports")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Report by Category")
        category_report = get_expenses_by_category()

        if category_report:
            df_category = pd.DataFrame(category_report, columns=["Category", "Total Amount"])
            st.dataframe(df_category, use_container_width=True)
        else:
            st.info("No category report data.")

    with col2:
        st.write("### Report by Payment Method")
        payment_report = get_expenses_by_payment_method()

        if payment_report:
            df_payment = pd.DataFrame(payment_report, columns=["Payment Method", "Total Amount"])
            st.dataframe(df_payment, use_container_width=True)
        else:
            st.info("No payment method report data.")