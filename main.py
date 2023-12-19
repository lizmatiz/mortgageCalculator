import streamlit as st
import pandas as pd

st.set_page_config(layout="centered", 
                   page_title="Mortgage Calculator",
                   page_icon="https://media.istockphoto.com/id/1369053959/vector/house.jpg?s=612x612&w=0&k=20&c=iA7YgnbjMT89OD8WDtINPoD6p4-sY-GVp1Tt0YdeqxA=")

st.header("Mortgage Amortization Schedule")

def getUserInput():
    loanRequest = {}
    loanRequest["principalLoanAmount"] = (st.number_input("Total Loan Amount: ")) # user input for the amount needed for the loan
    loanRequest["loanLength"] = (st.number_input("Length of Loan (in years): ") * 12.0) # user input for the time length of the loan
    loanRequest["interestRate"] = (((st.number_input("Interest Rate (yearly): ")) / 100) / 12) # user input for the interest rate
    return loanRequest


def calculateMonthlyPayment(loanRequest: dict):
    if (((1 + (loanRequest["interestRate"] / 12)) ** loanRequest["loanLength"]) - 1) != 0: # makes sure division by 0 does not occur
        loanRequest["monthlyPayment"] = ((loanRequest["principalLoanAmount"]) * ((loanRequest["interestRate"] * (1 + loanRequest["interestRate"]) ** loanRequest["loanLength"]) / (((1 + loanRequest["interestRate"]) ** loanRequest["loanLength"]) - 1))) # mortgage payment equation
    else:
        if loanRequest["loanLength"] != 0: # makes sure division by 0 does not occur
            loanRequest["monthlyPayment"] = ((loanRequest)["principalLoanAmount"] / loanRequest["loanLength"])
        else:
            loanRequest["monthlyPayment"] = 0
    return loanRequest

def main():
    loanRequest = getUserInput()
    loanRequest = calculateMonthlyPayment(loanRequest)

    MTDprincipalCount = 0 # these all keep track of the current count
    MTDinterestCount = 0
    MTDtotalCount = 0
    principalLoanAmountCount = loanRequest["principalLoanAmount"]


    listRows = [] # this causes the row names to be Month: num
    remainingPrincipalBalance = [] # this keeps track of the remaining principal balance
    principalPerMonth = [] # this keeps track of how much of the monthly payment is towards the principal balance
    interestPerMonth = [] # this keeps track of how much of the monthly payment is towards interest
    MTDprincipal = [] # this keeps track of the month to date principal payments
    MTDinterest = [] # this keeps track of the month to date interest payments
    MTDtotal = [] # this keeps track of the month to date total payments

    for l in range(int(loanRequest["loanLength"])): # loops through each month

        listRows.append("Month: " + str(l + 1)) # row names

        interestPerMonth.append(principalLoanAmountCount * loanRequest["interestRate"]) # interest monthly payment
        principalPerMonth.append(loanRequest["monthlyPayment"] - (interestPerMonth[l])) # principal monthly payment

        principalLoanAmountCount = principalLoanAmountCount - principalPerMonth[l] # remaining principal balance to be paid
        remainingPrincipalBalance.append(principalLoanAmountCount)
        
        MTDprincipalCount = MTDprincipalCount + principalPerMonth[l] # month to date principal payments
        MTDprincipal.append(MTDprincipalCount)

        MTDinterestCount = MTDinterestCount + interestPerMonth[l] # month to date interest payments
        MTDinterest.append(MTDinterestCount)

        MTDtotalCount = MTDtotalCount + loanRequest["monthlyPayment"] # month to date payments
        MTDtotal.append(MTDtotalCount)


    graph = pd.DataFrame( # data frame for the graph
        {"MTD Total": MTDtotal,
        "MTD Principal": MTDprincipal,
        "MTD Interest": MTDinterest,
        "Initial Loan Amount": loanRequest["principalLoanAmount"]}
    )

    st.line_chart(graph)

    table = pd.DataFrame( # data frame for the table
        {"Month": listRows,
        "Remaining Balance": remainingPrincipalBalance,
        "Monthly Payment": loanRequest["monthlyPayment"],
        "Monthly Principal": principalPerMonth,
        "Monthly Interest": interestPerMonth}
    )

    st.dataframe( # edits the numbers in the table
        table,
        width=800,
        column_config = {"Remaining Balance": st.column_config.NumberColumn(format="$ %.2f"),
                        "Monthly Payment": st.column_config.NumberColumn(format="$ %.2f"),
                        "Monthly Principal": st.column_config.NumberColumn(format="$ %.2f"),
                        "Monthly Interest": st.column_config.NumberColumn(format="$ %.2f")},
        hide_index=True,
    )

if __name__ == "__main__":
    main()