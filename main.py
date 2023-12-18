import streamlit as st
import pandas as pd

st.header("Mortgage Amortization Schedule")

principalLoanAmount = st.number_input("Total Loan Amount: ") # user input for the amount needed for the loan
loanLength = st.number_input("Length of Loan (in years): ") * 12.0 # user input for the time length of the loan
interestRate = ((st.number_input("Interest Rate (yearly): ")) / 100) / 12 # user input for the interest rate

if (((1 + (interestRate / 12)) ** loanLength) - 1) != 0: # makes sure division by 0 does not occur
    monthlyPayment = principalLoanAmount * ((interestRate * (1 + interestRate) ** loanLength) / (((1 + interestRate) ** loanLength) - 1)) # mortgage payment equation
else:
    if loanLength != 0: # makes sure division by 0 does not occur
        monthlyPayment = principalLoanAmount / loanLength
    else:
        monthlyPayment = 0

MTDprincipalCount = 0 # these all keep track of the current count
MTDinterestCount = 0
MTDtotalCount = 0
principalLoanAmountCount = principalLoanAmount

listRows = [] # this causes the row names to be Month: num
remainingPrincipalBalance = [] # this keeps track of the remaining principal balance
principalPerMonth = [] # this keeps track of how much of the monthly payment is towards the principal balance
interestPerMonth = [] # this keeps track of how much of the monthly payment is towards interest
MTDprincipal = [] # this keeps track of the month to date principal payments
MTDinterest = [] # this keeps track of the month to date interest payments
MTDtotal = [] # this keeps track of the month to date total payments

for l in range(int(loanLength)): # loops through each month

    listRows.append("Month: " + str(l + 1)) # row names

    interestPerMonth.append(principalLoanAmountCount * interestRate) # interest monthly payment
    principalPerMonth.append(monthlyPayment - (interestPerMonth[l])) # principal monthly payment

    principalLoanAmountCount = principalLoanAmountCount - principalPerMonth[l] # remaining principal balance to be paid
    remainingPrincipalBalance.append(principalLoanAmountCount)
    
    MTDprincipalCount = MTDprincipalCount + principalPerMonth[l] # month to date principal payments
    MTDprincipal.append(MTDprincipalCount)

    MTDinterestCount = MTDinterestCount + interestPerMonth[l] # month to date interest payments
    MTDinterest.append(MTDinterestCount)

    MTDtotalCount = MTDtotalCount + monthlyPayment # month to date payments
    MTDtotal.append(MTDtotalCount)


graph = pd.DataFrame( # data frame for the graph
    {"MTD Total": MTDtotal, "MTD Principal": MTDprincipal, "MTD Interest": MTDinterest, "Initial Loan Amount": principalLoanAmount}
)

st.line_chart(graph)

table = pd.DataFrame( # data frame for the table
    {"Month": listRows, "Remaining Balance": remainingPrincipalBalance, "Monthly Payment": monthlyPayment, "Monthly Principal": principalPerMonth, "Monthly Interest": interestPerMonth}
)

st.data_editor( # edits the numbers in the table
    table, column_config = {"Remaining Balance": st.column_config.NumberColumn(format="$ %.2f"), "Monthly Payment": st.column_config.NumberColumn(format="$ %.2f"), "Monthly Principal": st.column_config.NumberColumn(format="$ %.2f"), "Monthly Interest": st.column_config.NumberColumn(format="$ %.2f")},
    hide_index=True,
)