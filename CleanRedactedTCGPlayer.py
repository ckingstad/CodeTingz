# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 12:20:15 2022

@author: ckingstad
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 12:30:07 2022

@author: ckingstad
"""
import requests
import pandas as pd
import json
import csv
import io
import gspread_dataframe as gd
import gspread as gs

#pull in api keys from config file
public_key = 'REDACTED'
private_key = 'REDACTED'
APID = 'REDACTED'

#API connection information
response = requests.post(
            "https://api.tcgplayer.com/token",
            
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"},
           
            data=(f"grant_type=client_credentials"
                  f"&client_id="+public_key+"&"
                  f"client_secret="+private_key)
        )
response.json()
access = response.json()['access_token']
headers = {"accept": "application/json", 
           "Content-Type": "application/json",
           'User-Agent': 'PokemonPrices',
           "Authorization": "bearer " + access}
#2848 is EvolvSkies for GroupID
print('------------Product listing starts HERE---------')
df = pd.DataFrame(columns = ['productId', 'name','cleanName','imageUrl','categoryId','groupId', 'url','modifiedOn'])
offset=0
x = range(offset, 300, 100)
for n in x:
    url = "https://api.tcgplayer.com/catalog/products?categoryId=3&groupId=2848&offset="+str(n)+"&limit=100"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print('---------------this is my products------------------')
    print(data["results"])
    print(n)
    #df = pd.DataFrame(columns = ['productId', 'name','cleanName','imageUrl','categoryId','groupId', 'url','modifiedOn'])
    df = df.append(data["results"], ignore_index=True)
#find the products with group and catID
print('---------------this is my products------------------')
#print(df)
#print(len(df))
#create dataframe to then append the below results
df2 = pd.DataFrame(columns = ['productId', 'lowPrice', 'midPrice', 'highPrice', 'marketPrice', 'directLowPrice', 'subTypeName'])
for column in df[['productId']]:
    values = df[column].values.tolist()
    for value in values:
        #print(value)
        url = "https://api.tcgplayer.com/pricing/product/"+str(value)
        #print(url)
        response = requests.request("GET", url, headers=headers)
        #print(url)
        prices = response.json()
        #add this to a dataframe
        df2 = df2.append(prices["results"], ignore_index=True)
    print('close loop')
print('---------PRICING DF------------')
#print(df2)
print('------------DF DF---------------')
#print(df)
newnew= pd.merge(df, df2, how='left', on='productId')
newnew['loaddate']=pd.to_datetime('today').strftime("%Y-%m-%d")
print('-------PRINTING THAT NEWNEW----------')
print(newnew)
#google sheets 
newnew = newnew.replace(r'\n',' ', regex=True) 
df4 = newnew.fillna("")
print(df4)
data_list = df4.values.tolist()
print(data_list)
gc = gs.service_account(filename="REDACTED")
sh = gc.open("PokemonPricing")
sh.sheet1.append_rows(data_list)
print('-------------------completed to table-------------------')




