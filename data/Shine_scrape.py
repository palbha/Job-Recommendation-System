#Importing required skills
import bs4
import requests
import re
import pandas as pd
import numpy as np

#Creating a data frame  to store scrapped details
shinedf = pd.DataFrame(columns=['Title','Company','Experience','Location',
						   'Salary','Key_Skills','Posted_on','URL','Summary','JD'])

page_count = 1
for i in range(52):

	url = 'https://www.shine.com/job-search/data-science-jobs-{}?sort=1'.format(page_count)
		
	data  = requests.get(url)
	soup = bs4.BeautifulSoup(data.text,'html.parser')
	
	tags = soup.find_all('li',{'class':'search_listingleft search_listingleft_100'})
	
	
	for r in tags:
	
		title = r.find('li',{'class':'snp cls_jobtitle'}).text.strip()
		
		company = r.find('li',{'class':'snp_cnm cls_cmpname cls_jobcompany'}).text.strip()
			
		experience = r.find('span',{'class':'snp_yoe cls_jobexperience'}).text.strip()
		
		location = r.find('span',{'class':'locjsrp'}).text.strip()
		
		key_skills = r.find('em',{'class':'skl'}).text
		key_skills = re.sub('[\\xa0 \\n]+',' ',key_skills)
		
		posted =  r.find('li',{'class':'time share_links jobDate cls_job_date_format'}).text.strip()
		
		summary = r.find('li',{'class':'srcresult'}).text.strip()
		
		linktag = r.find('meta',{'itemprop':'url'})
		link = linktag.get('content')
					
		job  = requests.get(link)
		jobsoup = bs4.BeautifulSoup(job.text,'html.parser')
		
		try:
			salary = jobsoup.find('li',{'class':'cls_jobsalary'}).text
		except:
			salary = np.NAN
			
		job_des = jobsoup.find('div',{'class':'jobdescription pull-left'}).text
		job_des = re.sub('\\xa0',' ',job_des)
		
		shinedf = shinedf.append({'Title':title,'Company':company,'Experience':experience,'Location':location,
								   'Salary':salary,'Key_Skills':key_skills,'Posted_on':posted,
								   'URL':link,'Summary':summary,'JD':job_des}, ignore_index=True)
	
	page_count += 1

#Transfering data back to excel file
shinedf.to_excel('Shinejobs.xlsx')