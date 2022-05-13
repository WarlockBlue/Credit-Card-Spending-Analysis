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

FINANCEDATA = pd.read_csv("/Users/andres/Documents/Projects/Credit-Card-Spending-Analysis/Finances/Transactions.csv")


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
    
# CreditCardPivot.to_excel("/home/andres/sf_Data_Science_Projects/Finances/CreditCardPivot.xlsx")

print(CreditCardPivot)
    
MaxPivot = pd.pivot_table(CreditCard, values="Debit",index=["Year","Month"], aggfunc=max , sort=False)

MaxPivot=MaxPivot.unstack(0)

for column in MaxPivot.columns:
    
    largest2=MaxPivot[[column]][column].nlargest(2)
    print(largest2)
    print(CreditCard[CreditCard["Debit"]==largest2[0]])




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

#%% Ploting only one graph
plt.figure(figsize=(10,8))

BAR = sns.barplot(x="Month", y="Debit", data=CreditCard[CreditCard["Year"]==2021], \
                order=months , estimator=np.sum, ci=None)

BAR.set_xticklabels(BAR.get_xticklabels(),rotation = 45)
BAR.set_title("Total Spending per Month on  2021")
for container in BAR.containers:
    BAR.bar_label(container,rotation=45)

plt.savefig('/Users/andres/Documents/Projects/Credit-Card-Spending-Analysis/Finances/TotalSpending2021.png')

#%%Plotting a box graph
plt.figure(figsize=(8,6))

BOX = sns.boxplot(y="Month",x="Debit",data=CreditCard[CreditCard["Year"]==2021], order=months, showfliers=False)
BOX.set_title("Spending Distribution 2021")
    
plt.savefig('/Users/andres/Documents/Projects/Credit-Card-Spending-Analysis/Finances/SpendingDistribution2021.png')

    
    