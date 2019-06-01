# -*- coding: utf-8 -*-

#Importing the required modules
import bs4
import requests
import xlwt 
import re
import numpy as np
import pandas as pd

#Creating a workbook to store the scrapped data
workbook = xlwt.Workbook()  
sheet1 = workbook.add_sheet("Python")
#df = pd.DataFrame(columns=['TimeStamp','Tweet'])
times17 = pd.DataFrame(columns = ['job_title','company','experience','salary','location','job_posted','job_applicants','keyskills','url'])

c1 = 1
for page in range(3097,3647,10): # range(1,3647,10)
    for seq in range(page,page+10):
        
        url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=data%20science&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=data%20science&pDate=I&sequence='+ str(seq) + '&startPage=' + str(page)

        data  = requests.get(url)
        
        soup = bs4.BeautifulSoup(data.text,'html.parser')

        tag = soup('h2')

        job_url = []
        for t in tag:
            
            tag1 = t.find('a').get('href')
            
            url_new = tag1
            job_url.append(url_new)
                
            data1  = requests.get(url_new)
            soup1 = bs4.BeautifulSoup(data1.text,'html.parser')

            tag2 = soup1('h1',{'class':'jd-job-title'})[0]#.findAll('b').text
            job_title = tag2.text.strip()
            
            company = soup1('h2')[0].text.strip()
            
            exp = soup1('ul',{'class':'top-jd-dtl clearfix'})[0]#.findAll('li')
            w = exp.text.strip()
            w = re.sub('([\n\s]+\s)',',',w)
            w = w.split(',')
            experience = w[1]
            salary = w[3]
            location = w[-1]
            tag3 = soup1('strong')
            job_posted = tag3[3].text.strip()
            tag4 = soup1('strong',{'class':'ng-binding'})#,{'class':'ng-binding'})

            if tag4 == []:
                job_applicants = 0
            else:
                job_applicants = tag4[0]
            tag5 = soup1('span',{'class':'jd-skill-tag'})
            keyskills = ''
            for tg in tag5:
                if tg.text != None:
                    keyskills= keyskills + ',' + tg.text.strip()
            keyskills = keyskills.strip(',')
#Writing data to excel file    
            sheet1.write(c1,0,job_title)
            sheet1.write(c1,1,company)
            sheet1.write(c1,2,experience)
            sheet1.write(c1,3,salary)
            sheet1.write(c1,4,location)
            sheet1.write(c1,5,job_posted)
            sheet1.write(c1,6,job_applicants)
            sheet1.write(c1,7,keyskills)
            sheet1.write(c1,8,url_new)
            c1 +=1


            times17 = times17.append({'job_title':job_title,'company':company,'experience':experience,
                                    'salary':salary,'location':location,'job_posted':job_posted,
                                    'job_applicants':job_applicants,'keyskills':keyskills,'url':url_new},ignore_index = True)

#Saving the excel file data 
workbook.save("DataScience jobs.xls")
times17.to_excel("times17.xlsx", index=False)    
