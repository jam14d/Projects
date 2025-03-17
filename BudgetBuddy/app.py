import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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
            .metric-box { padding: 15px; border-radius: 10px; text-align: center; font-size: 18px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3); background: linear-gradient(145deg, #A88C7D, #B2A68D); color: white; margin-bottom: 10px; }
            .expense-box { padding: 15px; border-radius: 10px; text-align: center; font-size: 16px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3); background: linear-gradient(145deg, #7297A0, #82AC7C); color: white; margin-bottom: 5px; }
            h1, h2, h3 { background-color: #54738E; color: white; padding: 10px; border-radius: 10px; text-align: center; box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3); font-family: 'Roboto Slab', serif; }
            body::before { content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: url('https://www.transparenttextures.com/patterns/aged-paper.png'); opacity: 0; z-index: -1; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.title("Budget Buddy")
    st.markdown("---")
    
    # User-defined expenses with pre-filled values
    default_expenses = {
        "Rent": 0,  
        "Car Insurance": 0,  
        "Credit Card": 360,
        "Electricity": 43,
        "Water": 85,
        "Internet": 25,
        "Groceries": 175,
        "Gasoline": 60,  
        "Fun": 100,
        "Gym": 50,
        "Savings": 50,
        "Miscellaneous": 100,
    }
    
    expense_estimates = {}
    
    st.sidebar.header("Budget Settings")
    
    # Monthly income input
    income = st.sidebar.number_input("Monthly Income ($)", value=450 * 4, min_value=0, step=50)  
    
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
    
    col1, col2 = st.columns([1, 3])  # Makes col1 thinner, giving col2 more space

    with col1:
        st.markdown("### Budget Summary")
        st.markdown(f"<div class='metric-box'>Monthly Income: <b>${income}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>Total Expenses: <b>${total_expenses:.2f}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>Remaining Balance: <b>${remaining_balance:.2f}</b></div>", unsafe_allow_html=True)
        
        if remaining_balance < 0:
            st.error("Your expenses exceed your income! Consider adjusting your budget.")
        else:
            st.success("Your budget is balanced!")

        st.markdown("### Expense Details")
        for category, amount in expense_estimates.items():
            st.markdown(f"<div class='expense-box'><b>{category}:</b> ${amount:.2f}</div>", unsafe_allow_html=True)

    with col2:
        #st.markdown("### The Big Picture & The Fine Print: Budget Insights")
        if expense_estimates:
            fig = px.pie(
                names=expense_estimates.keys(), 
                values=expense_estimates.values(), 
                #title="Expense Distribution", 
                color_discrete_sequence=["#A88C7D", "#B2A68D", "#7297A0", "#54738E", "#82AC7C", "#9DBA94"]
            )
            

        # Earth-tone colors
        colors = [
            "#C19A6B",  # Camel
            "#B2A68D",  # Sand
            "#708090",  # Slate
            "#9DBA94",  # Sage
            "#A88C7D",  # Clay
            "#54738E",  # Dusty Blue
            "#7297A0",  # Stormy Sea
            "#D2B48C",  # Tan
            "#9E7B6E",  # Walnut
            "#BDB76B",  # Dark Khaki
            "#D3C0A3",  # Beige
            "#8F9779"   # Moss
        ]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(expense_estimates.keys()), 
                    values=list(expense_estimates.values()), 
                    hole=0.1,
                    textinfo='percent+label',
                    textfont=dict(size=14, color='white'),
                    marker=dict(colors=colors, line=dict(color='#2C2F33', width=1))
                )
            ]
        )

        fig.update_layout(
            width=1000,  # Increase figure width
            height=500,  # Increase figure height
            title={
                'text': "Who's Taking the Biggest Slice of Spending Pie?",
                'font': dict(color='white', size=20, family='Arial, sans-serif'),
                'x': 0.5
            },
            legend=dict(
                orientation="h",
                font=dict(color='white', size=15),
                x=0.5,
                xanchor='center',
                y=-1.0,
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',  # transparent background
            plot_bgcolor='rgba(0,0,0,0)',    # transparent background
            margin=dict(l=0, r=0, t=50, b=0)
        )

        fig.update_traces(
            textinfo='percent+label',
            textfont_size=14,
            marker=dict(line=dict(color='#000000', width=1))
        )

        st.plotly_chart(fig, use_container_width=True)

        # Convert expenses into a percentage of income
        expense_data = {
            "Category": list(expense_estimates.keys()),
            "Amount": list(expense_estimates.values()),
            #"Percentage of Income": [(amount / income) * 100 if income > 0 else 0 for amount in expense_estimates.values()]
        }

        df_expenses = pd.DataFrame(expense_data)

       
        # Bar Chart: Total Spending Per Category
        fig_bar = px.bar(df_expenses, 
                        x="Category", 
                        y="Amount", 
                        text_auto=".2s",
                        labels={"Amount": "Total Spent ($)"},
                        color="Category",
                        color_discrete_sequence=px.colors.qualitative.Set3)

        fig_bar.update_layout(
            title={
                'text': "How Many Dollars Go Where?",
                'font': dict(color='white', size=20, family='Arial, sans-serif'),  # Match pie chart title styling
                'x': 0.5  # Center the title
            },
            yaxis=dict(title="Total Spent ($)"),
            xaxis=dict(title="Spending Categories"),
            margin=dict(l=40, r=40, t=50, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(fig_bar, use_container_width=True)



if __name__ == "__main__":
    main()


#test