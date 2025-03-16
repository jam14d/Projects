#Expense Estimates for San Diego 
expense_estimates = {
    "Rent": 0,  # Covered
    "Car Insurance": 0,  # Covered
    "Utilities (Electricity, Water, Internet)": 120 + 85 + 50,
    "Groceries": 350,
    "Gasoline": round(5.06 * (14.5 * 0.5), 2),  # RAV4: Half a tank per month (~7.25 gallons)
    "Dining Out & Entertainment": 100,
    "Health & Wellness": 50,
    "Savings": 50,
    "Miscellaneous": 100,
}

# Calculate total expenses and remaining balance
income = 450 * 4  # Monthly unemployment income ($1800)
total_expenses = sum(expense_estimates.values())
remaining_balance = income - total_expenses

print(f"My monthly income is ${income}")

# Print Budget Summary
print("\n*** Budget Summary (Hardcoded for Southern California) ***")
for category, amount in expense_estimates.items():
    print(f"{category}: ${amount:.2f}")

print(f"\nTotal Expenses: ${total_expenses:.2f}")
print(f"Remaining Balance: ${remaining_balance:.2f}")
