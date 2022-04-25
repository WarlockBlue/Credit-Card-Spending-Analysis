# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 22:40:34 2022

@author: Andres
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

FINANCEDATA = pd.read_csv("/home/andres/sf_Data_Science_Projects/Transactions.csv")


FINANCEDATA = FINANCEDATA.drop("Check Number", axis = 1)

CreditCard = FINANCEDATA[FINANCEDATA["Account Running Balance"].isna()] \
    .drop(["Account Running Balance","Transaction Type"], axis=1).reset_index(drop=True)
    
print(CreditCard.head())

print(CreditCard.shape)



CreditCard["Date"] = pd.to_datetime(CreditCard["Date"])

CreditCard["Year"] = CreditCard["Date"].dt.year

CreditCard["Month"] = CreditCard["Date"].dt.month_name()

CreditCard["Day"] = CreditCard["Date"].dt.day



CreditCard= CreditCard[CreditCard["Debit"].notna()].drop("Credit", axis=1)

CreditCard = CreditCard[~CreditCard["Debit"].str.contains("[a-zA-Z]")]

CreditCard["Debit"] = pd.to_numeric(CreditCard["Debit"])

months=[]

for x in range(1,13):
    months.append(calendar.month_name[x])
    
CreditCardPivot = CreditCard.pivot_table(values = "Debit", index = ["Year","Month"], \
                                         aggfunc=[max,np.mean,np.sum], sort=False)
print(CreditCardPivot)

#%% Seaborn Visualization

sns.set_style("whitegrid")
plt.figure(figsize=(15,20))

MAX = sns.catplot(x="Month", y="Debit", col="Year", col_wrap=3, data=CreditCard, \
                kind="bar", order=months , estimator=np.max, ci=None)
    
MAX.set_titles(col_template = "Maximum Spending in {col_name}", y=1.03)

MAX.set(yticks=np.arange(0,5500,500))

MAX.set_xticklabels(rotation = 45)

# MAX.savefig('C:/Users/Andres/Desktop/Data Science Projects/Finances/MaximumCreditCardSpending.png')



MEAN = sns.catplot(x="Month", y="Debit", col="Year", col_wrap=3, data=CreditCard, \
                kind="bar", order=months , estimator=np.mean, ci=None)
    
MEAN.set_titles(col_template = "Average Spending in {col_name}", y=1.03)

MEAN.set(yticks=np.arange(0,275,25))

MEAN.set_xticklabels(rotation = 45)

# MEAN.savefig('C:/Users/Andres/Desktop/Data Science Projects/Finances/AverageCreditCardSpending.png')


TOTAL = sns.catplot(x="Month", y="Debit", col="Year", col_wrap=3, data=CreditCard, \
                kind="bar", order=months , estimator=np.sum, ci=None)
    
TOTAL.set_titles(col_template = "Total Spending in {col_name}", y=1.03)

TOTAL.set(yticks=np.arange(0,6500,500))

TOTAL.set_xticklabels(rotation = 45)

# TOTAL.savefig('C:/Users/Andres/Desktop/Data Science Projects/Finances/TotalCreditCardSpending.png')