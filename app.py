import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="AI Pump Tracker",
    page_icon="⛽",
    layout="wide"
)

# Initialize Session State
if "sales_data" not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(
        columns=[
            "Date",
            "Machine",
            "Opening Reading",
            "Closing Reading",
            "Liter Price",
            "Total Liters",
            "Total Revenue",
        ]
    )

if "expense_data" not in st.session_state:
    st.session_state.expense_data = pd.DataFrame(
        columns=["Date", "Category", "Amount", "Description"]
    )

# Header
st.title("⛽ AI Pump Tracker & Management System")
st.markdown(
    "Manage your fuel machines, sales, expenses, and track profits efficiently."
)
st.divider()

# Sidebar
st.sidebar.header("📥 Data Entry Panel")

menu = st.sidebar.radio(
    "Go To Section",
    ["Dashboard & Analytics", "Add Machine Sales", "Add Expenses"],
)

# ------------------- SALES -------------------
if menu == "Add Machine Sales":

    st.subheader("📝 Record Machine Sales")

    with st.form("sales_form", clear_on_submit=True):

        date = st.date_input("Select Date", datetime.now())

        machine = st.selectbox(
            "Select Machine / Nozzle",
            [
                "Machine 01 (Petrol-Super)",
                "Machine 02 (Petrol-Super)",
                "Machine 03 (Diesel-Euro)",
            ],
        )

        opening = st.number_input(
            "Opening Meter Reading (Liters)",
            min_value=0.0,
            step=0.1,
        )

        closing = st.number_input(
            "Closing Meter Reading (Liters)",
            min_value=0.0,
            step=0.1,
        )

        price_per_liter = st.number_input(
            "Price Per Liter (PKR)",
            min_value=0.0,
            step=0.1,
        )

        submit_sales = st.form_submit_button("Save Sales Record")

        if submit_sales:

            if closing >= opening:

                liters_sold = closing - opening
                total_revenue = liters_sold * price_per_liter

                new_sales = pd.DataFrame(
                    [
                        {
                            "Date": date,
                            "Machine": machine,
                            "Opening Reading": opening,
                            "Closing Reading": closing,
                            "Liter Price": price_per_liter,
                            "Total Liters": liters_sold,
                            "Total Revenue": total_revenue,
                        }
                    ]
                )

                st.session_state.sales_data = pd.concat(
                    [st.session_state.sales_data, new_sales],
                    ignore_index=True,
                )

                st.success(
                    f"🎉 Sales recorded for {machine}! Total Liters Sold: {liters_sold:.2f} L"
                )

            else:
                st.error(
                    "❌ Closing reading cannot be less than opening reading."
                )

# ------------------- EXPENSES -------------------
elif menu == "Add Expenses":

    st.subheader("💸 Record Pump Expenses")

    with st.form("expense_form", clear_on_submit=True):

        exp_date = st.date_input("Select Date", datetime.now())

        category = st.selectbox(
            "Expense Category",
            [
                "Staff Salary",
                "Electricity / Utilities",
                "Maintenance",
                "Government Taxes / Fees",
                "Other",
            ],
        )

        amount = st.number_input(
            "Amount (PKR)",
            min_value=0.0,
            step=10.0,
        )

        description = st.text_input("Short Description")

        submit_expense = st.form_submit_button("Save Expense Record")

        if submit_expense:

            if amount > 0:

                new_expense = pd.DataFrame(
                    [
                        {
                            "Date": exp_date,
                            "Category": category,
                            "Amount": amount,
                            "Description": description,
                        }
                    ]
                )

                st.session_state.expense_data = pd.concat(
                    [st.session_state.expense_data, new_expense],
                    ignore_index=True,
                )

                st.success(
                    f"💰 Expense of PKR {amount:,.2f} recorded successfully!"
                )

            else:
                st.error("❌ Amount must be greater than zero.")

# ------------------- DASHBOARD -------------------
else:

    total_revenue = st.session_state.sales_data["Total Revenue"].sum()
    total_expenses = st.session_state.expense_data["Amount"].sum()
    net_profit = total_revenue - total_expenses

    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Total Revenue", f"PKR {total_revenue:,.2f}")
    col2.metric("📉 Total Expenses", f"PKR {total_expenses:,.2f}")

    if net_profit >= 0:
        col3.metric("📈 Net Profit", f"PKR {net_profit:,.2f}")
    else:
        col3.metric("🚨 Net Loss", f"PKR {net_profit:,.2f}")

    st.divider()

    st.subheader("📊 Visual Analytics")

    c1, c2 = st.columns(2)

    with c1:

        summary_df = pd.DataFrame(
            {
                "Category": ["Revenue", "Expenses"],
                "Amount": [total_revenue, total_expenses],
            }
        )

        if total_revenue > 0 or total_expenses > 0:

            fig = px.bar(
                summary_df,
                x="Category",
                y="Amount",
                color="Category",
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No financial data available.")

    with c2:

        if not st.session_state.sales_data.empty:

            machine_df = (
                st.session_state.sales_data.groupby("Machine")[
                    "Total Revenue"
                ]
                .sum()
                .reset_index()
            )

            fig2 = px.pie(
                machine_df,
                values="Total Revenue",
                names="Machine",
                hole=0.4,
            )

            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info("No sales data available.")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Sales Log Book")
        st.dataframe(
            st.session_state.sales_data,
            use_container_width=True,
        )

    with right:
        st.subheader("Expenses Log Book")
        st.dataframe(
            st.session_state.expense_data,
            use_container_width=True,
        )

# Footer
st.markdown("---")

st.markdown(
    "<h4 style='text-align:center;color:#7f8c8d;'>Developed by: Engr Akas Gurmani</h4>",
    unsafe_allow_html=True,
          )
