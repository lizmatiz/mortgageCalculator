import streamlit as st
import pandas as pd
import numpy as np

st.header("Mortgage Amortization Schedule")

principalLoanAmount = st.number_input("Total Loan Amount: ")
loanLength = st.number_input("Length of Loan (in years): ") * 12.0
interestRate = ((st.number_input("Interest Rate: ")) / 100) / 12

if (((1 + (interestRate / 12)) ** loanLength) - 1) != 0:
    monthlyPayment = principalLoanAmount * ((interestRate * (1 + interestRate) ** loanLength) / (((1 + interestRate) ** loanLength) - 1))
else:
    monthlyPayment = 0

listRows = []

MTDprincipalCount = 0
MTDinterestCount = 0

remainingPrincipalBalance = []
principalPerMonth = []
interestPerMonth = []
paymentPerMonth = []
MTDprincipal = []
MTDinterest = []
MTDtotal = []

for l in range(int(loanLength)):

    listRows.append("Month: " + str(l + 1))

    interestPerMonth.append(principalLoanAmount * interestRate)
    principalPerMonth.append(monthlyPayment - (interestPerMonth[l]))
    paymentPerMonth.append(monthlyPayment)

    principalLoanAmount = principalLoanAmount - principalPerMonth[l]
    remainingPrincipalBalance.append(principalLoanAmount)
    
    MTDprincipalCount = MTDprincipalCount + principalPerMonth[l]
    MTDprincipal.append(MTDprincipalCount)

    MTDinterestCount = MTDinterestCount + interestPerMonth[l]
    MTDinterest.append(MTDinterestCount)

dfTable = pd.DataFrame(
    {"Remaining Principal Balance": remainingPrincipalBalance, "Monthly Payment": paymentPerMonth, "Monthly Principal": principalPerMonth, "Monthly Interest": interestPerMonth}
)

dfTable.index = listRows

st.table(dfTable)