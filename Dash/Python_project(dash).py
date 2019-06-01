#Importing libraries useful for successfull execution of the below code

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from dash.dependencies import Input, Output, State
import os
import flask
import mysql.connector
import numpy as np
import re
from operator import itemgetter
from io import BytesIO
import base64
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

#Connecting to database since our data from web scarpping has been stored in mysql jobs database
def DatabaseConnection(user,passwd,database):
   try:
	   mydb = mysql.connector.connect(host = 'localhost',
							  user = user,
							  passwd = passwd,
							  db = database
							  #,auth_plugin="mysql_native_password"
							  )

   except:
	   print("""The login credentials you entered are not valid for
		   the database you indicated.  Please check your login details and try
		   again.""")
   return mydb

mydb=DatabaseConnection('--username','--password','jobs')
mycursor=mydb.cursor()

dataset=pd.read_sql("select * from jobs",mydb )
print(dataset.columns)

#Function club_loc has been used to clean the Location column
def club_loc(c):
	c = c.lower().strip()
	if 'mumbai' in c:
		c ='mumbai'
	elif 'thane' in c or 'mulund' in c:
		c ='mumbai'
	elif re.findall('b[ea]ngal[uo]r[ue]',c):
		c = 'bangalore'
	elif 'pune' in c:
		c ='pune'
	elif re.findall('guru?g[aon]',c):
		c = 'gurugram'
	elif 'delhi' in c:
		c ='delhi'
	elif 'chennai' in c:
		c ='chennai'
	elif 'ahmedabad' in c:
		c ='ahmedabad'
	elif 'thiruvananthapuram' in c:
		c ='thiruvananthapuram'
	elif 'chandigarh' in c:
		c ='chandigarh'
	elif 'surat' in c:
		c ='surat'
	elif re.findall('mysor[eu]',c):
		c = 'mysore'
	elif 'indore' in c:
		c ='indore'
	elif 'mohali' in c:
		c ='mohali'
	elif 'visakhapatnam' in c:
		c ='visakhapatnam'
	elif 'vadodara' in c:
		c ='vadodara'
	elif 'salem' in c:
		c ='salem'
	elif 'lucknow' in c:
		c ='lucknow'
	elif 'gandhinagar' in c:
		c ='gandhinagar'
	elif 'faridabad' in c:
		c ='faridabad'
	elif 'bhopal' in c:
		c ='bhopal'
	elif re.findall('bhubanesh?war',c):
		c = 'bhubaneshwar'

	return c.title()

# List of locations to be included as foreign cities
foreign_list=["united arab emirates",
'australia',
'afghanistan',
'bulgaria',
'cairo',
'chile',
'colombia',
'czech',
'denmark',
'dubai',
'hong',
'indonesia',
'israel',
'italy',
'japan',
'jeddah',
'kuwait',
'lithuania',
'london',
'california',
'maldives',
'morocco',
'netherlands',
'nigeria',
'oman',
'philippines',
'portland',
'raleigh',
'seattle',
'slovakia',
'south africa',
'sri lanka',
'taiwan',
'thailand',
'turkey',
"qatar" ,
"hong kong",
"indoneisa",
"phillipines",
"malaysia",
"sweden",
"argentina",
"new jersey",
"spain",
"mexico",
"myanmar",
"romania",
"poland",
"norway",
"finland",
"uk",
'united kingdom',
"usa",
'us',
'uruguay',
'united states of america',
"vietnam",
"austria",
"south korea",
"switzerland",
"brazil",
"belgium",
"texas",
"singapore",
"illinois",
"new york",
"hungary",
"china",
"russia",
"france",
"california"
"bulgaria",
"romania",
"pakistan",
"costa rica",
"germany",
"portugal",
"canada",
"abu",
"ireland",
"maryland"]

# Function club is used to clean key_skills column in dataset
def club(w):
	if 'python' in w:
		w='python'
	elif "busi" in w and "analy" in w:
		w='business analytics'
	elif "stat" in w and "analy" in w:
		w='statistical analytics'
	elif "data" in w and 'analy' in w:
		w='data analytics'
	elif 'analy' in w:
		w='data analytics'
	elif 'data scientist' in w:
		w='data scientist'
	elif 'algo' in w:
		w='algorithm'
	elif 'hadoop' in w:
		w='hadoop'
	elif 'ml' in w or 'machine' in w:
		w='machine learning'
	elif 'nlp' in w or 'natural' in w:
		w='NLP'
	elif w.startswith('r') and 'prog' in w:
		w='r language'
	elif w.startswith('r') and w.endswith('r'):
		w='r language'
	elif re.findall('^big', w):
		w='big data'
	elif 'db' in w or 'database' in w:
		w='database'
	elif w=='com' or w=='technology':
		w=' '
	return w.title()

#Function tidy is used to convert text in appropriate form
def tidy(x):
	x = re.sub("[\'\"\-\/]+","", x)
	x = x.lower()
	x = list(set((','.join([club(w.strip()) for w in x.split(',')])).split(',')))
	x = ','.join(w for w in x)
	return x

dataset['keyskills2'] = dataset['keyskills'].apply(lambda x: tidy(x))
# Binning Jobs as Indian/not:
dataset["in_india"]=1

def in_india(x):
	if x in foreign_list:
		return 0
	else:
		return 1

dataset["in_india"] = dataset['location'].apply(lambda x: in_india(x.lower()))


#Calculating count for each Skill
skills = (','.join(dataset['keyskills2'])).split(',')
skills_dict = {}
for i in skills:
	if i in skills_dict:
		skills_dict[i] += 1
	else:
		skills_dict[i] = 1

#Skill column being sorted
skills_10= sorted(skills_dict.items(), key = itemgetter(1), reverse = True)
skills_10 = pd.DataFrame(skills_10, columns=['Skills','Freq'])
skills_10=skills_10[skills_10["Skills"]!=""]
skills_10 = skills_10.iloc[:10]

#Calculating count of job as per Location
dataset['location2'] = dataset['location'].apply(lambda x: club_loc(x))
loc_india = dataset[dataset['in_india']==1]
location_dict = {}
for i in loc_india['location2']:
	if i == 'India':
		continue
	elif i in location_dict:
		location_dict[i] += 1
	else:
		location_dict[i] = 1


loc_10= sorted(location_dict.items(), key = itemgetter(1), reverse = True)
loc_10 = pd.DataFrame(loc_10, columns=['Location','Count'])
loc_10 = loc_10.iloc[:10]


#Functions to calculate similarity

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def get_cosine_sim(*strs):
	vectors = [t for t in get_vectors(*strs)]

	sim = cosine_similarity(vectors)
	return round(float(sim[0,1]),4)

def get_vectors(*strs):
	text = [t for t in strs]

	vectorizer = CountVectorizer(text)
	vectorizer.fit(text)
	return vectorizer.transform(text).toarray()


#Creating new key_skills column in cleansed form as compared to the scrapped one

dataset['keyskills2'] = dataset['keyskills'].apply(lambda x: tidy(x))

#This function has been used to create a HTML table from pandas dataframe as per Job recommendation button
def make_dash_table(df):

	table = []
	html_head=[]


	table.append(html.Th("Title"))
	table.append(html.Th("Company"))
	table.append(html.Th("Posted On"))
	table.append(html.Th("Skill"))
	table.append(html.Th("Url"))
	table_x=[]

	#lets take length(table) with headers
	len_table=len(table)

	while True :
		for index, row in df.iterrows():
			html_row = []
			html_row_x=[]
			for i in range(0,len(row)):
				if i==(len(row)-1):
					html_row.append(html.Td(html.A(href=row[i], children="Apply")))
				else:

					html_row.append(html.Td([row[i]]))
				html_row_x.append([row[i]])

			if html_row_x not in table_x:
				table.append(html.Tr(html_row))


			table_x.append(html_row_x)
			#Condition so as to display only top 10 rows :
			if len(table)>(len_table+9):
				return table
				#break

	return table



# The below function has been used to display HTML table as per Skill recommendation button
def make_str(df):

	table = []
	html_row=[]

	table.append(html.Th("Skills"))
	for i in range (0,len(df)):
		html_row=[]
		html_row.append(html.Td([df.iloc[i,0]]))
		table.append(html.Tr(html_row))


	return table



def print_button():
	printButton = html.A(['Print PDF'],className="button no-print print",style={'position': "absolute", 'top': '-40', 'right': '0'})
	return printButton

def Header():
	return html.Div([
		get_logo(),
		get_header(),
		html.Br([]),
		get_menu()
	])

def serve_layout():

	return html.Div([
			html.Div(id='state-container', style={'display': 'none'}),
			html.Div(id='output'),
			dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i} for i in ['A', 'B']])
		])

#Show logo alongside header
def get_logo():
	logo = html.Div([

		html.Div([
			html.Img(src='https://smedia2.intoday.in/btmt/images/stories/jobs-660_012019080005.jpg', height='60', width='160')
		], className="ten columns padded"),


	], className="row gs-header")
	return logo


def get_header():
	header = html.Div([

		html.Div([
			html.H5(
				'Job Reccomendation Made Easy')
		], className="twelve columns padded")

	], className="row gs-header gs-text-header")
	return header


def get_menu():
	menu = html.Div([

		dcc.Link('Overview   ', href='/jrc/overview', className="tab first"),

		dcc.Link('Job Trend Analysis   ', href='/jrc/job_analysis', className="tab"),

		dcc.Link('Location Wise Trends  ', href='/jrc/loc_wise', className="tab"),

		dcc.Link('Distributions   ', href='/jrc/dist', className="tab"),

		dcc.Link('Time Series Analysis ', href='/jrc/tra', className="tab")

	], className="row ")
	return menu

#Initializing dash application
app = dash.Dash(__name__)

server = app.server


skills = dataset['keyskills'].apply(lambda x: tidy(x))
skills = np.array(skills).flatten()

skills_str = ','.join(skills)
skills = skills_str.split(',')

skills_dict = {}
for i in skills:
	#print("i is ",i.strip())
	if i in skills_dict:
		skills_dict[i] += 1
	else:
		skills_dict[i] = 1

from operator import itemgetter
d= sorted(skills_dict.items(), key = itemgetter(1), reverse = True)

#Colors for plotly graphs
color=[]
for i in range(0,10):
	if skills_10.iloc[i,1]==skills_10.iloc[:,1].max():
		color.append('rgb(0, 191, 255)')
	else:
		color.append('rgba(204,204,204,1)')



app.layout = serve_layout

app.config.supress_callback_exceptions = True

#First page layout
overview = html.Div([  # page 1

		print_button(),

		html.Div([
			Header(),

			# Row 3
			html.Div([
				html.Div([
				html.H6(["Job data"],
							className="gs-header gs-table-header padded"),
				html.Label('Enter your name'),
				dcc.Input(id='name_ip'),

				html.Label('Enter your preferred job location'),
				dcc.Input(id='loc_ip'),

				html.Label('Enter your experience(0-9)'),
				dcc.Input(id='exp_ip'),

				html.Label('Enter your key skills'),
				dcc.Input(id='skill_ip'),

				html.Label(' '),
				html.Div([
				html.Button(' Job Recommendation',id='button-1'),
				html.Button(' Skill Reccomendation',id='button-2'),
				]),
				html.Div(id='output'),
				html.Div(id='output2'),

				]),



			], className="row "),
			], className="subpage")

	])

#Skill recommendation page layout
skill_rec=html.Div([
			Header(),

			html.Div([

				html.Div([
							html.H6(["Skill wise Trend Analysis"],className="gs-header gs-table-header padded")]
							,className="row "),
							html.Div([
							dcc.Graph(
								id='graph-2',
								figure={
								'data':[go.Bar(
								x=skills_10.iloc[:,0],
								y=skills_10.iloc[:,1],
								marker=dict(
								color=color),
						   )],
							'layout': {
							'clickmode': 'event+select',
							'title':'Top Trending Skills'
							}
							}
							),


			],className="row "),
			], className="subpage1")
		])


loc_wise=html.Div([
			Header(),

			html.Div([

				html.Div([
							html.H6(["Location wise Trend Analysis"],className="gs-header gs-table-header padded")]
							,className="row "),
							html.Div([
							dcc.Graph(
								id='graph-2',
								figure={
								'data':[go.Bar(
								x=loc_10.iloc[:,0],
								y=loc_10.iloc[:,1],
								marker=dict(
								color=color),
						   )],
							'layout': {
							'clickmode': 'event+select'
							}
							}
							),


			],className="row "),
			], className="subpage1")
		])


#covert Posted on columns in original dataset into TimeStamp
dataset['Posted on'] = pd.to_datetime(dataset['Posted on'],infer_datetime_format=True)
#slicing for jobs in India
df_new = dataset[dataset['in_india']==1]
timeseries = df_new['Posted on'].groupby(df_new['Posted on']).count()

time_color = []
for i in range(len(timeseries)):
	x = np.random.randint(50,200,3)
	time_color.append('rgb({},{},{})'.format(x[0],x[1],x[2]))

time_size = timeseries.apply(lambda x: (x/max(timeseries))*100)

d=pd.DataFrame(dataset['min_exp(yrs)'].groupby(dataset['min_exp(yrs)']).count())
labels = d.index.values
val = d['min_exp(yrs)']

#Layout for Job count distribution per year
dist=html.Div([
			Header(),

			#dcc.Link('', href='/jrc/job_analysis', className="tab"),
			# Row 3
			html.Div([
				html.Div([
				html.H6(["Distribution of job as per Years of Experience"],
							className="gs-header gs-table-header padded")],className="row "),
				html.Div([
							dcc.Graph(
								id='graph-4',
								figure={
								'data':[go.Pie(
								labels=labels,
								values=val,
								name= "Years of Experience",
								hoverinfo='label+value+percent+name'
						   )],
						'layout': {
							'height': 500,
							'clickmode': 'event+select'
							}
							}
							),

				],className="row ")


			], className="subpage1")
		])

#Layout for time series trend for job openings
tra=html.Div([
			Header(),

			#dcc.Link('', href='/jrc/job_analysis', className="tab"),
			# Row 3
			html.Div([
				html.Div([
				html.H6(["Time Series Trends"],
							className="gs-header gs-table-header padded")],className="row "),
				html.Div([
							dcc.Graph(
								id='graph-3',
								figure={
								'data':[go.Scatter(
								x=timeseries.index,
								y=timeseries,
								mode='markers',
								marker=dict(
								color=time_color,
								size=time_size),
						   )],
						'layout': {
							'height': 500,
							'clickmode': 'event+select'
							}
							}
							),

				],className="row ")


			], className="subpage1")
		])


#Overall job trend analysis
job_analysis=html.Div([
			Header(),

			#dcc.Link('', href='/jrc/job_analysis', className="tab"),
			# Row 3
			html.Div([
				html.Div([
				html.H6(["Job Trends"],
							className="gs-header gs-table-header padded")],className="row "),
				html.Div([
							dcc.Graph(
								id='graph-2',
								figure={
								'data':[go.Bar(
								x=skills_10.iloc[:,0],
								y=skills_10.iloc[:,1],
								marker=dict(
								color=color),
						   )],
						'layout': {
							'height': 500,
							'clickmode': 'event+select'
							}
							}
							),

				],className="row ")


			], className="subpage1")
		])


#App callback determing the flow of button-1 i.e Job recommendation
@app.callback(
	Output('output', 'children'),
	[Input('button-1','n_clicks')],
	state=[State('name_ip', 'value'),
	State('loc_ip', 'value'),
	State('exp_ip', 'value'),
	State('skill_ip', 'value')])

def compute(n_clicks, name_1, loc_1, exp_1,skill_1):
	if ((name_1==None) or (loc_1==None) or (exp_1==None)or (skill_1==None)):
		return None
	else:
		output_flag=1
		user_skills = tidy(skill_1)
		loc_2 = club_loc(loc_1)


		filtered_data = dataset[(dataset['location2']==loc_2) & (dataset['min_exp(yrs)']<=int(exp_1)) & (dataset['max_exp(yrs)']>=int(exp_1))]
		filtered_data['skill_sim']=0
		filtered_data['skill_sim'] = filtered_data['keyskills2'].apply(lambda x: get_cosine_sim(x,user_skills))
		filtered_data = filtered_data.sort_values(by = 'skill_sim',ascending = False)


		A = filtered_data[['title','company','Posted on','keyskills2',"url"]][filtered_data['skill_sim']>0]


		return html.Div([
				'Recomendations',
				html.Table(make_dash_table(A))
				])


#App callback determing the flow of button-2 i.e Skill recommendation
@app.callback(
	Output('output2', 'children'),
	[Input('button-2','n_clicks')],
	state=[State('name_ip', 'value'),
	State('loc_ip', 'value'),
	State('exp_ip', 'value'),
	State('skill_ip', 'value')])

def compute_2(n_clicks, name_1, loc_1, exp_1,skill_1):
	if ((name_1==None) or (loc_1==None) or (exp_1==None)or (skill_1==None)):
		return None
	else:
		output_flag=2
		user_skills = tidy(skill_1)
		loc_2 = club_loc(loc_1)
		filtered_data = dataset[(dataset['location2']==loc_2) & (dataset['min_exp(yrs)']<=int(exp_1)) & (dataset['max_exp(yrs)']>=int(exp_1))]
		filtered_data['skill_sim']=0
		filtered_data['skill_sim'] = filtered_data['keyskills2'].apply(lambda x: get_cosine_sim(x,user_skills))
		filtered_data = filtered_data.sort_values(by = 'skill_sim',ascending = False)
		list1=[]
		dict1={}
		for i in range(0,len(filtered_data)):
			for k in filtered_data.iloc[i,10].split(","):
				flag=0
				for l in user_skills.split(","):
					if k ==l:
						flag =1
				if flag!=1:
					if k not in dict1.keys():
						dict1[k]=1
					else :
						dict1[k]=dict1[k]+1

					if k not in list1:
						list1.append(k)

		list2=[]
		for i , j in dict1.items():

			list2.append([i,j])


		df1=pd.DataFrame(list2,columns=["skill","count"])
		df2=df1.iloc[:10,]

		df3=df2.sort_values(by = 'count',ascending = False)
		print(df3)

		return make_str(df3)


# In case any individual tried to open an improper path ..
noPage = html.Div([  # 404

	html.P(["404 Page not found"])

	], className="no-page")



# Describing the layout, or the UI, of the app
app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])




@app.callback(dash.dependencies.Output('page-content', 'children'),
			  [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
	if (pathname == '/jrc' or pathname == '/jrc/overview'):
		return overview
	elif pathname=='/jrc/job_analysis':
		return job_analysis
	elif pathname=='/jrc/skill_rec':
		return skill_rec
	elif pathname=='/jrc/loc_wise':
		return loc_wise
	elif pathname=='/jrc/tra':
		return tra
	elif pathname=='/jrc/dist':
		return dist
	else:
		return noPage


#Calling all the css files being used in our application

css_directory = os.getcwd()
stylesheets = ['css1.css','css2.css','css3.css']
static_css_route = '/static/'


@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
	if stylesheet not in stylesheets:
		raise Exception(
			'"{}" is excluded from the allowed static files'.format(
				stylesheet
			)
		)
	return flask.send_from_directory(css_directory, stylesheet)


for stylesheet in stylesheets:
	app.css.append_css({"external_url": "/static/{}".format(stylesheet)})

#Calling all the javascripts files being used in our application

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
			   "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
	app.scripts.append_script({"external_url": js})



if __name__ == '__main__':
	app.run_server(debug=True)
