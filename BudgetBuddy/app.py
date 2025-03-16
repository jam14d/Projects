import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(page_title="Budget Buddy", layout="wide")
    
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&display=swap');
            body { background-color: #B2A68D; color: #2C2F33; }
            .big-font { font-size:22px !important; font-weight: bold; }
            .stButton>button { width: 100%; background-color: #A88C7D; color: white; border-radius: 10px; box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3); }
            .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #9DBA94; color: white; border-radius: 5px; border: 1px solid #7297A0; padding: 10px; box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.1); }
            .metric-box { padding: 20px; border-radius: 10px; text-align: center; font-size: 18px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3); background: linear-gradient(145deg, #A88C7D, #B2A68D); color: white; }
            h1, h2, h3 { background-color: #54738E; color: white; padding: 10px; border-radius: 10px; text-align: center; box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3); font-family: 'Roboto Slab', serif; }
            body::before { content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: url('https://www.transparenttextures.com/patterns/aged-paper.png'); opacity: 100; z-index: -1; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.title("Budget Buddy")
    st.markdown("---")
    
    # User-defined expenses with pre-filled values
    default_expenses = {
        "Rent": 0,  # Covered
        "Car Insurance": 0,  # Covered
        "Credit Card": 360,
        "Electricity": 43,
        "Water": 85,
        "Internet": 25,
        "Groceries": 175,
        "Gasoline": 60,  # RAV4: Half a tank per month (~7.25 gallons)
        "Dining Out & Entertainment": 100,
        "Gym": 50,
        "Savings": 50,
        "Miscellaneous": 100,
    }
    
    expense_estimates = {}
    
    st.sidebar.header("Budget Settings")
    
    # Monthly income input
    income = st.sidebar.number_input("Monthly Income ($)", value=450 * 4, min_value=0, step=50)  # Default: $1800
    
    st.sidebar.header("Add or Update Expenses")
    for category, default_value in default_expenses.items():
        expense_estimates[category] = st.sidebar.number_input(f"{category}", value=default_value, min_value=0, step=10)
    
    # Option to add new categories
    new_category = st.sidebar.text_input("New Category Name")
    new_category_value = st.sidebar.number_input("Amount for New Category", value=0, min_value=0, step=10)
    
    if st.sidebar.button("Add Category") and new_category:
        expense_estimates[new_category] = new_category_value
    
    # Calculate total expenses and remaining balance
    total_expenses = sum(expense_estimates.values())
    remaining_balance = income - total_expenses
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### Budget Summary")
        st.markdown(f"<div class='metric-box'>Monthly Income: <b>${income}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>Total Expenses: <b>${total_expenses:.2f}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>Remaining Balance: <b>${remaining_balance:.2f}</b></div>", unsafe_allow_html=True)
        
        if remaining_balance < 0:
            st.error("Your expenses exceed your income! Consider adjusting your budget.")
        else:
            st.success("Your budget is balanced!")
    
    with col2:
        st.markdown("### Expense Breakdown")
        if expense_estimates:
            fig = px.pie(names=expense_estimates.keys(), values=expense_estimates.values(), title="Expense Distribution", color_discrete_sequence=["#A88C7D", "#B2A68D", "#7297A0", "#54738E", "#82AC7C", "#9DBA94"])
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("## Expense Details")
    for category, amount in expense_estimates.items():
        st.write(f"- **{category}**: ${amount:.2f}")
    
if __name__ == "__main__":
    main()
