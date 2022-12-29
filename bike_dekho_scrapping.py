
# Used libraries

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time



# driver

url ='https://www.bikedekho.com/new-bikes'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
r=requests.get(url,headers=headers).text
driver = webdriver.Firefox()
driver.get(url)

time.sleep(5)



# clicking "View All Brands" button

button = driver.find_elements(By.XPATH, "//span[contains(text(),'View All Brands')]")
button[0].click()

time.sleep(5)


# Defining Soup

soup = BeautifulSoup(driver.page_source,"html.parser")



# Getting all the links of bike companies

links_company = []
whitebox = soup.find_all('li', class_ = 'gsc_col-xs-4 gsc_col-sm-3 gsc_col-md-3 gsc_col-lg-2')

for i in range(len(whitebox)):
    A = whitebox[i].find_all('a',href = True)
    for i in A:
        links_company.append('https://www.bikedekho.com'+ i['href'])




# appending values in different lists 


company_name = []
bike_name  = []
price = []
milege = []
links_bike = []
for i in links_company:
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    r=requests.get(i,headers=headers).text
    soup = BeautifulSoup(r,'lxml')
    len_bike = len(soup.find_all('div', class_ = 'gsc_col-sm-12 gsc_col-xs-12 gsc_col-md-8 listView holder posS'))
    A = soup.find_all('h3')[0:len_bike]

    for i in range(len_bike):
        # bike_name
        try:
            bike_name.append(soup.find_all('h3')[i].text)
        except:
            bike_name.append('Na')
        # price
        try:
            price.append(soup.find_all('div',class_ = 'price')[i].text)
        except:
            price.append('Na')
        # milege
        try:
            if 'kmpl' in  soup.find_all('div',class_ = 'dotlist')[i].text :
                M =  soup.find_all('div',class_ = 'dotlist')[i].text
                milege.append((M.split(" ")[0]))
            else:
                milege.append('Na')
        except:
            milege.append('Na')
        # company_name
        try:
            company_name.append(soup.find_all('h1')[0].text)
        except:
            company_name.append("Na")
     # links_bike   
    
    for i in range(len_bike): # getting link of the bikes from companies
        for link in A[i].find_all('a',href = True):
            links_bike.append('https://www.bikedekho.com'+ link['href'])


# appending values in different lists from above "links_bike"

Engine = []
power = []
Torque = [] 

for i in links_bike:
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    r=requests.get(i,headers=headers).text
    soup = BeautifulSoup(r,'lxml')
    # Engine
    try:
        for i in soup.find_all('td', class_ = 'gsc_col-xs-12 textHold')[0]:
            
            Engine.append(i.text)
    except:
        Engine.append('Na')
    # power

    try:
        j = soup.find_all("td",{"class" : "gsc_col-xs-12 textHold"})

        if 'PS'  in j[1].text:
            power.append(j[1].text)
        elif 'PS'  in j[2].text:
            power.append(j[2].text)
        elif 'PS' in j[3].text:
            power.append(j[3].text)
        elif 'PS'  in j[4].text:
            power.append(j[4].text)
        elif 'PS' in j[5].text:
            power.append(j[5].text)
        else:
            power.append('NA')
            
            
    except:
        power.append('Na')
    Torque
    try:
        j = soup.find_all("td",{"class" : "gsc_col-xs-12 textHold"})

        if 'Nm'  in j[1].text:
            Torque.append(j[1].text)
        elif 'Nm'  in j[2].text:
            Torque.append(j[2].text)
        elif 'Nm'  in j[3].text:
            Torque.append(j[3].text)
        elif 'Nm' in j[4].text:
            Torque.append(j[4].text)
        elif 'Nm' in j[5].text:
            Torque.append(j[5].text)
        else:
            Torque.append('NA')        
    except:
        Torque.append('Na')

# Into data frame 

col=['company_name','bike_name','price','milege','Engine','power','Torque'] 
df=pd.DataFrame({'company_name': company_name, 'bike_name': bike_name,'price':price,'milege':milege,'Engine':Engine,'power':power,'Torque':Torque})

# max and min price 

df[['min_price', 'max_price']] = df.price.str.split("-", expand = True)
df = df.drop(columns = ['price'])

# removing electric bike's data

df=df[~df['power'].isin(['Na'])]
df=df[~df['power'].isin(['NA'])]



# to csv 

df.to_csv(r'#laptop_path \bike_dekho_2.csv')


# print df

print(df)
