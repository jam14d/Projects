import streamlit as st
import pandas as pd
import ollama  # ✅ Import Ollama for local LLM

# Function to analyze budget using Ollama LLM
def analyze_budget(expenses, income):
    prompt = f"""
    Here is a user's monthly budget:

    Income: ${income}

    Expenses:
    {expenses.to_string(index=False)}

    Analyze this budget and provide insights, suggestions for savings, and whether this budget is sustainable.
    """

    response = ollama.chat(
        model="mistral",  # ✅ Use local Mistral model
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# Streamlit UI
st.title("💰 AI-Powered Budget Calculator")

income = st.number_input("Enter your monthly income ($)", min_value=0.0, step=50.0)
st.write("### Enter Your Expenses")

# Expense input
num_expenses = st.number_input("How many expense categories?", min_value=1, step=1, value=3)
expense_data = []

for i in range(int(num_expenses)):
    col1, col2 = st.columns([2, 1])
    with col1:
        category = st.text_input(f"Expense {i+1} Category", key=f"cat_{i}")
    with col2:
        amount = st.number_input(f"Amount for {category} ($)", min_value=0.0, step=10.0, key=f"amt_{i}")
    expense_data.append({"Category": category, "Amount": amount})

# Convert to DataFrame
expenses_df = pd.DataFrame(expense_data)

# Display entered expenses
if not expenses_df.empty:
    st.subheader("📊 Your Expenses")
    st.dataframe(expenses_df)

# Run analysis
if st.button("Analyze Budget"):
    if income > 0 and not expenses_df.empty:
        analysis = analyze_budget(expenses_df, income)
        st.subheader("💡 Budget Insights")
        st.write(analysis)
    else:
        st.error("Please enter a valid income and expenses before analyzing.")
