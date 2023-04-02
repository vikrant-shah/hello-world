# -*- coding: utf-8 -*-
"""
Spyder Editor

Data Quality - Accuracy POC Data RPA_ion Script
"""


import pandas as pd
#from pandas import DataFrame as df

df = pd.read_csv('final_output.csv', index_col = 0)
#df.columns = df.columns.str.replace(' ','')
df.columns = ['File_AccountNumber','File_PrincipalBalance','File_InterestRate','File_PaymentStartDate','File_MaturityDate','File_PaymentAmount']
df.drop_duplicates(subset=['File_AccountNumber'], keep='first',inplace=True)

#AccountNumber (non-word chara can be followed by 0 always)
df['RPA_AccountNumber'] = df['File_AccountNumber'].str.extract(r'(\d{2}\W\d{8})',expand = False) #2digits,non-word character,8 digits
df['RPA_AccountNumber'] = df['RPA_AccountNumber'].str.replace(r'\W[0-9]','') #replace non-word followed any digit
df = df[df['RPA_AccountNumber'].notna()]


#PrincipalBalance
df['RPA_PrincipalBalance'] = df['File_PrincipalBalance'].str.replace(',','')
df['RPA_PrincipalBalance'] = df['RPA_PrincipalBalance'].str.extract(r'^([1-9]\d+\.\d{1,2})',expand = False) 
#non-zero first digit, followed by one or more (+)number of digits, period and 1 to 2 digits
#Compare only int for principal balance not float

#InterestRate
df['RPA_InterestRate'] = df['File_InterestRate'].str.extract(r'(\d{1,2}[\.,]\d{2,3})',expand=False)
df['RPA_InterestRate'] = df['RPA_InterestRate'].str.replace(',','.')
#df['RPA_InterestRate'] = df['RPA_InterestRate'].str.rstrip('%')
# 1 to 2 digits followed by . or , followed by one or more (+) digits

monthshort="jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
monthlong="nuary|ruary|rch|ril|may|une|uly|gust|tember|ober|vember|cember"
monthnamelong_dict = {'nuary':'01','ruary':'02','rch':'03','ril':'04','may':'05','une':'06','uly':'07','gust':'08','tember':'09','ober':'10','vember':'11','cember':'12'}
monthnameshort_dict = {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','jun':'06','jul':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'}


#PaymentStartDate (Assume dd is always 1)
df['File_PaymentStartDate']= df['File_PaymentStartDate'].str.lower() 
payment_df = df['File_PaymentStartDate'].str.extract(r'((' + monthshort + ')[-](\d{2}))|((' + monthlong +').*(20\d{2}))', expand = False)
payment_df.columns = ['Pat1Date','Pat1MonthName','Pat1yyyy','Pat2Date','Pat2MonthName','Pat2yyyy']

payment_df['Pat1Month'] = payment_df['Pat1MonthName'].map(monthnameshort_dict)
payment_df['Pat2Month'] = payment_df['Pat2MonthName'].map(monthnamelong_dict)
payment_df.loc[payment_df['Pat1yyyy'].notna(), 'Pat1yyyy'] = "20" + payment_df['Pat1yyyy'].astype(str)
payment_df['Pat1Month'].update(payment_df.pop('Pat2Month'))
payment_df['Pat1yyyy'].update(payment_df.pop('Pat2yyyy'))


payment_df['PaymentStartDate1'] = payment_df['Pat1yyyy'].astype(str) + "-" + payment_df['Pat1Month'].astype(str) + "-1"
df['RPA_PaymentStartDate'] = payment_df['PaymentStartDate1'].str.replace('nan-nan-1','')


#MaturityDate
df['File_MaturityDate']= df['File_MaturityDate'].str.lower()
maturity_df = df['File_MaturityDate'].str.extract(r'((' + monthshort + ')[-]([2-9][2-9]))|((' + monthlong +').*(20\d{2}))', expand = False)
maturity_df.columns = ['Pat1Date','Pat1MonthName','Pat1yyyy','Pat2Date','Pat2MonthName','Pat2yyyy']

maturity_df['Pat1Month'] = maturity_df['Pat1MonthName'].map(monthnameshort_dict)
maturity_df['Pat2Month'] = maturity_df['Pat2MonthName'].map(monthnamelong_dict)
maturity_df.loc[maturity_df['Pat1yyyy'].notna(), 'Pat1yyyy'] = "20" + maturity_df['Pat1yyyy'].astype(str)

#maturity_df['Pat1dd'].update(maturity_df.pop('Pat2dd'))
maturity_df['Pat1Month'].update(maturity_df.pop('Pat2Month'))
maturity_df['Pat1yyyy'].update(maturity_df.pop('Pat2yyyy'))


maturity_df['MaturityDate1'] = maturity_df['Pat1yyyy'].astype(str) + "-" + maturity_df['Pat1Month'].astype(str) + "-1"
#hardcoded 1 as dd
df['RPA_MaturityDate'] = maturity_df['MaturityDate1'].str.replace('nan-nan-1','')


#PaymentAmount
df['RPA_PaymentAmount'] = df['File_PaymentAmount'].str.replace(',','')
df['RPA_PaymentAmount'] = df['RPA_PaymentAmount'].str.extract(r'([$is5]\d+\.\d{1,2})',expand = False)
df['RPA_PaymentAmount'] = df['RPA_PaymentAmount'].str.replace(r'^[$is5]','')
#df['RPA_PaymentAmount'] = df['RPA_PaymentAmount'].str.lstrip('s$')

'''
#index_account = df[df['Account Number'].isna()].index
#df.dropna(subset=['AccountNumber'], inplace=True)
#dftest = DataFrame(df['AccountNumber'],df['PrincipalBalance'])
'''

#df.to_csv('RPASnowflakeUpload.csv')
