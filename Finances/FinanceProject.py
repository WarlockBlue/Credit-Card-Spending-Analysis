# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 21:03:48 2022

@author: Andres
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

FINANCEDATA = pd.read_csv("C:/Users/Andres/Desktop/Data Science Projects/Finances/Transactions.csv")
# print(FINANCEDATA.nunique())

FINANCEDATA = FINANCEDATA.drop("Check Number", axis = 1)

# print(FINANCEDATA.head(n=10))

# DebitCard = FINANCEDATA[FINANCEDATA["Account Running Balance"].notna()] \
#     .drop(["Account Running Balance","Transaction Type"], axis=1).reset_index(drop=True)
# print(DebitCard.head())
# print(DebitCard.shape)

CreditCard = FINANCEDATA[FINANCEDATA["Account Running Balance"].isna()] \
    .drop(["Account Running Balance","Transaction Type"], axis=1).reset_index(drop=True)
    
print(CreditCard.head())
print(CreditCard.shape)
print(CreditCard[CreditCard["Debit"]=="952.37"])

#%% Credit Card Expenses Analysis

CreditCard["Date"] = pd.to_datetime(CreditCard["Date"])
CreditCard["Year"] = CreditCard["Date"].dt.year
CreditCard["Month"] = CreditCard["Date"].dt.month_name()
# CreditCard["Month"] = CreditCard["Date"].dt.month
CreditCard["Day"] = CreditCard["Date"].dt.day
# print(CreditCard[CreditCard["Debit"]=="952.37"])

# CreditCard["Debit"] = pd.to_numeric(CreditCard["Debit"],errors="coerce")
# CreditCard["Credit"] = CreditCard["Credit"].astype(float,errors="ignore")


CreditCardSpending = CreditCard[CreditCard["Debit"].notna()].drop("Credit", axis=1)
CreditCardSpending = CreditCardSpending[~CreditCardSpending["Debit"].str.contains("[a-zA-Z]")]
CreditCardSpending["Debit"] = pd.to_numeric(CreditCardSpending["Debit"])

# print(CreditCardSpending[CreditCardSpending["Debit"]==952.37])
CreditCardPayments = CreditCard[CreditCard["Debit"].isna()].drop("Debit", axis=1)

months=[]

for x in range(1,13):
    months.append(calendar.month_name[x])

# print(CreditCardSpending[CreditCardSpending["Debit"].str.contains("[a-zA-Z]")])
# print(CreditCardSpending[CreditCardSpending["Debit"].str.isalpha()])

SpendingMaxPerMonth = CreditCardSpending[["Year","Month","Debit"]].groupby(["Year","Month"]).max()
# SpendingMaxPerMonth = CreditCardSpending.pivot_table(index="Month",columns="Year",values="Debit", aggfunc="max", sort=False)
# SpendingMaxPerMonth["Month"] = SpendingMaxPerMonth["Month"].dt.month_name()

# SpendingMaxPerMonth = CreditCardSpending[["Year","Month","Description","Debit"]].sort_values(by=["Debit","Month","Year"])
print(SpendingMaxPerMonth[["Debit"]])

# print(SpendingMaxPerMonth.iloc[0])
# print(SpendingMaxPerMonth)

SpendingTotalPerMonth = CreditCardSpending[["Year","Month","Debit"]].groupby(["Year","Month"]).sum()
# print(SpendingTotalPerMonth)

SpendingAveragePerMonth = CreditCardSpending[["Year","Month","Debit"]].groupby(["Year","Month"]).mean()
# print(SpendingAveragePerMonth)

#%% Seaborn Visualization
sns.set_style("whitegrid")
g = sns.catplot(x="Month", y="Debit", col="Year", data=CreditCardSpending, kind="bar", order=months , estimator=np.max, ci=None)
g.set_titles(col_template = "Maximum Spending in {col_name}", y = 1.03)
g.set(yticks=np.arange(0,5500,500))
g.set_xticklabels(rotation = 45)
