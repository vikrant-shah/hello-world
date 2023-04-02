# -*- coding: utf-8 -*-
"""
Spyder Editor

Data Quality - Accuracy POC Data RPA_ion Script
"""


import pandas as pd
#from pandas import DataFrame

df = pd.read_csv('final_output.csv', index_col = 0)
#df.columns = df.columns.str.replace(' ','')
df.columns = ['File_AccountNumber','File_PrincipalBalance','File_InterestRate','File_PaymentStartDate','File_MaturityDate','File_PaymentAmount']


#AccountNumber
df['RPA_AccountNumber'] = df['File_AccountNumber'].str.extract(r'^(\d{2}-\d{8})',expand = False)
df['RPA_AccountNumber'] = df['RPA_AccountNumber'].str.replace(r'-[0-9]','')

#PrincipalBalance
df['RPA_PrincipalBalance'] = df['File_PrincipalBalance'].str.replace(',','')
df['RPA_PrincipalBalance'] = df['RPA_PrincipalBalance'].str.extract(r'^([1-9]\d+\.00)',expand = False)

#InterestRate
df['RPA_InterestRate'] = df['File_InterestRate'].str.extract(r'^(\d+\.\d+\%)',expand=False)
df['RPA_InterestRate'] = df['RPA_InterestRate'].str.rstrip('%')


monthshort="jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
monthlong="january|february|march|april|may|june|july|august|september|october|november|december"
monthnamelong_dict = {'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}
monthnameshort_dict = {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06','jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'}


#PaymentStartDate
df['File_PaymentStartDate']= df['File_PaymentStartDate'].str.lower()
payment_df = df['File_PaymentStartDate'].str.extract(r'((\d{1,2})[-](' + monthshort + ')[-](\d{2}))|((' + monthlong +')\s*(\d{1,2})[,]\s*(20\d{2}))', expand = False)
payment_df.columns = ['Pat1Date','Pat1dd','Pat1MonthName','Pat1yyyy','Pat2Date','Pat2MonthName','Pat2dd','Pat2yyyy']

payment_df['Pat1Month'] = payment_df['Pat1MonthName'].map(monthnameshort_dict)
payment_df['Pat2Month'] = payment_df['Pat2MonthName'].map(monthnamelong_dict)
payment_df.loc[payment_df['Pat1yyyy'].notna(), 'Pat1yyyy'] = "20" + payment_df['Pat1yyyy'].astype(str)

payment_df['Pat1dd'].update(payment_df.pop('Pat2dd'))
payment_df['Pat1Month'].update(payment_df.pop('Pat2Month'))
payment_df['Pat1yyyy'].update(payment_df.pop('Pat2yyyy'))


payment_df['PaymentStartDate1'] = payment_df['Pat1yyyy'].astype(str) + "-" + payment_df['Pat1Month'].astype(str) + "-"  + payment_df['Pat1dd'].astype(str)
df['RPA_PaymentStartDate'] = payment_df['PaymentStartDate1'].str.replace('nan-nan-nan','')


#MaturityDate
df['File_MaturityDate']= df['File_MaturityDate'].str.lower()
maturity_df = df['File_MaturityDate'].str.extract(r'((\d{1,2})[-](' + monthshort + ')[-]([2-9][2-9]))|((' + monthlong +')\s*(\d{1,2})[,]\s*(20\d{2}))', expand = False)
maturity_df.columns = ['Pat1Date','Pat1dd','Pat1MonthName','Pat1yyyy','Pat2Date','Pat2MonthName','Pat2dd','Pat2yyyy']

maturity_df['Pat1Month'] = maturity_df['Pat1MonthName'].map(monthnameshort_dict)
maturity_df['Pat2Month'] = maturity_df['Pat2MonthName'].map(monthnamelong_dict)
maturity_df.loc[maturity_df['Pat1yyyy'].notna(), 'Pat1yyyy'] = "20" + maturity_df['Pat1yyyy'].astype(str)

maturity_df['Pat1dd'].update(maturity_df.pop('Pat2dd'))
maturity_df['Pat1Month'].update(maturity_df.pop('Pat2Month'))
maturity_df['Pat1yyyy'].update(maturity_df.pop('Pat2yyyy'))


maturity_df['MaturityDate1'] = maturity_df['Pat1yyyy'].astype(str) + "-" + maturity_df['Pat1Month'].astype(str) + "-"  + maturity_df['Pat1dd'].astype(str)
df['RPA_MaturityDate'] = maturity_df['MaturityDate1'].str.replace('nan-nan-nan','')


#PaymentAmount
df['RPA_PaymentAmount'] = df['File_PaymentAmount'].str.replace(',','')
df['RPA_PaymentAmount'] = df['RPA_PaymentAmount'].str.extract(r'([$s58]\d+\.\d{2})',expand = False)
df['RPA_PaymentAmount'] = df['RPA_PaymentAmount'].str.replace(r'^\S','')
df['RPA_PaymentAmount'] = df['RPA_PaymentAmount'].str.lstrip('s$')

'''
#index_account = df[df['Account Number'].isna()].index
#df.dropna(subset=['AccountNumber'], inplace=True)
#dftest = DataFrame(df['AccountNumber'],df['PrincipalBalance'])
'''

df.to_csv('RPASnowflakeUpload.csv')
