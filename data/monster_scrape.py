# -*- coding: utf-8 -*-
#Importing the required modules

import requests
import bs4
import xlwt
from xlwt import Workbook
import re
import math

#here in monster there are many times data is coming in different form in the same tag and hence we have made sure to update data keeping the same in mind

url='https://www.monsterindia.com/data-scientist-r-python-tableau-hadoop-spark-spss-sas-scala-bigdata-data-analyst-data-science-statistics-business-analyst-machine-learning-jobs.html'
data=requests.get(url)
soup=bs4.BeautifulSoup(data.text,'html.parser')

count=soup.find('div',{'class':'count pull-left'})
count=count.text
count=re.findall('([0-9]*)\sJ',count)
count=int(count[0])

monster=[]

#for 1st page
job_counter=1
jobs_per_page=1
url='https://www.monsterindia.com/data-scientist-jobs.html'
data=requests.get(url)
soup=bs4.BeautifulSoup(data.text,'html.parser')
results=soup.findAll('div',{'class':'jobwrap'})
for res in results:

    error_flag=0
    #job title
    a=res.find('a',{'class':'title_in'})
    title=a['title']

    #job link
    job_link=a['href']
    job_link=job_link.replace('//','')

    #company name
    try:
        a=res.find('a',{'class':'jtxt orange'})
        company=a['title']
    except:
        span=res.find('div',{'class':'jtxt orange'})
        company=span.text
    #key skills
    div=res.findAll('div',{'class':'jtxt'})
    div_title=div[3]
    keyskills=div_title['title']
    #summary
    try:
        summary=div[4].text

    except:
        summary=res.findAll('div',{'class':'jtxt'})
        error_flag=1
    #location
    try:
        location=div[5].text

    except:

        error_flag=1
    #experince
    try:
        exp=res.findAll('div',{'class':'jtxt jico ico2'})


        exp=exp[0].text
    except:
        exp=res.findAll('div',{'class':'jtxt jico ico2'})
        error_flag=1
        
    #date
    try:
        date=res.find('div',{'class':'job_optitem ico7'})

        date=date.text
        date=re.findall(': ([0-9A-Za-z]*\s[A-Za-z]*\s[0-9]*)',date)
        date=date[0]
        error_flag=0
    except:
        date=res.find('div',{'class':'job_optitem ico7'})
        error_flag=1

    job_counter+=1
    jobs_per_page+=1
    if error_flag==0:
        monster.append((title,company,keyskills,summary,location,exp,date,job_link))
    else:
        error_flag=0
    if jobs_per_page==41:
        break
#from 2nd page
page_counter=2
#job_counter=40
while(page_counter<=math.ceil(count/40)):
    url='https://www.monsterindia.com/data-scientist-r-python-tableau-hadoop-spark-spss-sas-scala-bigdata-data-analyst-data-science-statistics-business-analyst-machine-learning-jobs-'+str(page_counter)+str('.html')
    data=requests.get(url)
    soup=bs4.BeautifulSoup(data.text,'html.parser')
    results=soup.findAll('div',{'class':'jobwrap'})
    jobs_per_page=1
    for res in results:
        #job title
        a=res.find('a',{'class':'title_in'})
        title=a['title']

        #job link
        job_link=a['href']
        job_link=job_link.replace('//','')

        #company name
        try:
            a=res.find('a',{'class':'jtxt orange'})
            company=a['title']

        except:
            span=res.find('div',{'class':'jtxt orange'})
            company=span.text

        #key skills
        try:
            div=res.findAll('div',{'class':'jtxt'})
            div_title=div[3]
            keyskills=div_title['title']
            
        except:
            print("no key skills present")
        #summary
        try:
            summary=div[4].text
            
        except:
            summary=res.findAll('span')

            error_flag=1
        #location
        try:
            location=div[5].text

        except:
            error_flag=1
        #experince
        try:
            exp=res.findAll('div',{'class':'jtxt jico ico2'})
            exp=exp[0].text

        except:
            exp=res.findAll('div',{'class':'jtxt jico ico2'})

            error_flag=1
        try:
            date=res.find('div',{'class':'job_optitem ico7'})
            date=date.text
            date=re.findall(': ([0-9A-Za-z]*\s[A-Za-z]*\s[0-9]*)',date)
            date=date[0]
           
            error_flag=0
        except:
            date=res.find('div',{'class':'job_optitem ico7'})
            
            error_flag=1
        
        if error_flag==0:
            monster.append((title,company,keyskills,summary,location,exp,date,job_link))
        else:
            error_flag=0
        job_counter+=1
        jobs_per_page+=1
        if jobs_per_page==41:
            break
    page_counter+=1

        

import pandas as pd
monster_data=pd.DataFrame(monster,columns=['title','company','keyskills','summary','location','exp','date','job_link'])

print(monster_data.shape)
print(monster_data.head())
monster_data.describe()
monster_data=monster_data.drop_duplicates()
monster_data.shape

#Saving the data back to excel
monster_data.to_excel("monster_data.xlsx")