#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 12:40:48 2022

@author: koreynishimoto
"""

import pandas as pd
import plotly.express as px
import numpy as np

from dataprep.clean import clean_phone,validate_phone



import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table

import dash_bootstrap_components as dbc

app = dash.Dash(__name__,meta_tags=[...])




app = dash.Dash(
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
      )

app.title = 'Takehome Test'


#############################################################
## Scrub Data##


pd.options.display.max_columns=200

df = pd.read_csv('/Users/koreynishimoto/Desktop/Takehome/'
                   +'takehomedata.csv', index_col=False)

#df = df.fillna('None')




df[['state','work state']]
state= np.where(df["state"] == df["work state"], True, False)
np.count_nonzero(state)


############################################################
##Clean Phone number##
############################################################

df['phone'] = df['phone'].str.replace(')',') ')

#some phone numbers have 9 characters. This is possiblle due to a leading
#0 which the computer deleted. ex: 04 = 4
df['phone']=df['phone'].str.zfill(10)
df['work phone']=df['work phone'].str.zfill(10)


#clean numbers
df=clean_phone(df, "phone", output_format="national")
df=clean_phone(df, "work phone", output_format="national")

sixth_column = df.pop('phone_clean')
fourteenth_column = df.pop('work phone_clean')
df.insert(6, 'Phone clean', sixth_column)
df.insert(14, 'Work phone clean', fourteenth_column)


df["valid phone"] = validate_phone(df["phone"])

df["Phone clean"].fillna(df["phone"], inplace=True)
df["Work phone clean"].fillna(df["work phone"], inplace=True)

seventh_column = df.pop('valid phone')
df.insert(7, 'Valid phone', seventh_column)




############################################################
#split date from time
############################################################


df[['Date']] = df['account created on'].str.split(expand=True)[0]


df['Year created'] = df['Date'].str.replace('.*(?<=/)', '', regex=True)


accountcount = df['Year created'].value_counts(dropna=False).reset_index(drop=False)

accountcount.columns=['Year created', 'Count']
accountcount=accountcount.sort_values(by='Year created')





############################################################
#Duplicates
############################################################


''' This section would be deleted after generating the report and
has only been kept for reviewing purposes of the test.

df.drop_duplicates(keep = False, inplace = True)

#Checking for duplicates of important information

#Showed 723 duplicated names. This includes NA
df.drop_duplicates(subset ="name",keep = False, inplace = True)


#No shared emails with shared name
dupname = df[df.duplicated(subset='name',keep=False)]
dupname = dupname[dupname.duplicated(subset='phone',keep=False)]

#No shared Phone numbers with shared name. This includes NA
dupname = dupname[dupname.duplicated(subset='phone',keep=False)]

dupname = dupname.sort_values('name')


#Showed 436 duplicate emails. Important when advertising since
#only one person may get the advertisement. 32 are NaN

dupemail = df[df.duplicated(subset='email',keep=False)]
df[df.duplicated(subset='email',keep=False)]['email'].isnull().value_counts()

# Showed there are 25 duplicated phone numbers. No overlap with missing emails. 
dupphone = df[df.duplicated(subset='Phone clean',keep=False)]

#no duplicated work email but missing 30. May be better to send emails this way.
dupwork = df[df.duplicated(subset='work email',keep=False)]


#no duplicate work phone numbers but missing 31. Call this way.
dupworkp = df[df.duplicated(subset='Work phone clean',keep=False)]
print(len(dupephone))


#691 duplicate work
dupwork = df[df.duplicated(subset='work',keep=False)]
dupwork = dupwork.sort_values('work')
print(dupwork)

dupwork['work'].value_counts()

dupwork.loc[dupwork['work']=='Smith and Sons']['work state'].value_counts()


#shows data frame as ordered by company name
city = dupwork['work'].value_counts(dropna=False).reset_index(drop=False)
city.columns = ['Work', 'Count']
city = city.sort_values('Work')


Adamsgroup = df.loc[df['work']=='Adams Group'][['work','state','work state','Year created']]

AdamsInc = df.loc[df['work']=='Adams Inc'][['work','state','work state','Year created']]

AdamsLLC = df.loc[df['work']=='Adams LLC'][['work','state','work state','Year created']]

AdamsPLC = df.loc[df['work']=='Adams PLC'][['work','state','work state','Year created']]


'''


############################################################
#Split first and last Name
############################################################


df[['First Name','Last Name']]=df.name.str.split(expand=True)


second_column = df.pop('First Name')
third_column = df.pop('Last Name')
df.insert(1, 'First Name', second_column)
df.insert(2, 'Last Name', third_column)

#Finding rows with no name.
emptyname = df[df["name"].isnull()][df.columns[df.isnull().any()]]
print('There are ' + str(len(emptyname)) + ' rows with no name. These rows can be found with the indexs' 
      + str(list(emptyname.index.values)))





############################################################
#split email to account and server name
############################################################



df[['Email Name','Server']]=df['email'].str.split('@',expand=True)

emailcount=df['Server'].value_counts(dropna=False)



print( ' There are ' + str(len(df[df['email'].isnull()].sort_values('Year created'))) + 
                           " emails that are NA.")

print( ' There are ' + str(len(df[df['phone'].isnull()])) +
                               " phone numbers are NA")
print( ' There are ' + str(len(df[df['address'].isnull()])) +
                               " address numbers are NA")



############################################################
#Choropleth Map
############################################################


code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}

df['Code'] = df['state'].map(code)

df=df.join(df['Code'].value_counts(), on='Code', lsuffix='', rsuffix =' Count')



mapfig = px.choropleth(data_frame = df, 
                    locations = 'Code',
                    locationmode = 'USA-states',
                    color = 'Code Count',
                    hover_name = "state",  
                    height = 800,
                    range_color = (150,230),
                    scope='usa'
                    )

mapfig.update_layout(
            plot_bgcolor="#011833",
            paper_bgcolor="#022248",
            geo_bgcolor="#011833",
            font=dict(color="white"),
            )



###############################################################################
#Line chart for accounts created over the years
#############################################################################


df=df.join(df['Year created'].value_counts(), on='Year created', lsuffix='', rsuffix =' count')

accounts = px.line(
             data_frame = accountcount,
             x = 'Year created',
             y = 'Count', 
             )



###############################################################################
#bar graph for most accounts opened per city
#############################################################################


city_account_count = df['city'].value_counts(dropna=False).reset_index(drop=False)

city_account_count.columns=['City', 'Count']


top_cities = px.bar(data_frame = city_account_count,
             x = 'City',
             y = 'Count',
             orientation = 'h'            
             )











#############################################################################
#start of styling of dashboard
#############################################################################


colors = {"background": "#011833", "text": "#7FDBFF"}

template = 'plotly_dark'


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#022248",
    "text": "#7FDBFF",
    
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    "background-color": "#022248",
    "text": "#7FDBFF",
    'borderWidth':0,
   
}




sidebar = html.Div(
    [
        html.H2("Take-home Exam", className="display-4"),
        html.Hr(),
        html.P(
            "Pick a category you would like displayed", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Account Information", href="/Account-Information", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        
        
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), sidebar, content],
                      style={'backgroundColor': colors['background'],
                             'color': colors['text'],
                             
                             },)



#############################################################################
#creating call back for side bar
#############################################################################





@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])


def render_page_content(pathname):
    if pathname == "/":
        return [ 
            
        dbc.Row([  
               dbc.CardImg(src=app.get_asset_url('img2.jpg'),
                    style={'height':'6cm', 'width' : '14cm','textAlign': 'center'}),
               
                    
               
                dbc.Col(
                    dbc.Card(
                            dbc.CardBody(
                                [  
                                    html.H5("Take-home Exam Dashboard", className="card-title"),
                                    html.P(
                                        'Using python, write some assessment and cleaning routines. '+
                                        'Provide a short write-up of what you observe about the data, how to review for reasonableness, and how to correct any errors or inconsistencies. ' 
                                        'Submit all your code, notes, and altered. ' 
                                        ),
                                    dbc.Button("FHB's Website", size="lg", id= 'Button-1', style={'backgroundColor':"#022248"},href="https://www.fhb.com/en/personal"),
                                    ]
                                ),
                            style={'backgroundColor': "#011833",'height':'6cm'},
                          ),
                  width=6),
                
                
                    ],
                ),
            
            html.Div('The table below is a summary of important information.  '
                   ),
            
            dash_table.DataTable(
                    id='table',
                    columns=[
                        {'name': 'Category',
                         'id': 'column1'
                         },
                        {'name': 'Name',
                         'id': 'column2'
                         },
                        {'name': 'Info',
                         'id': 'column3'
                         },
                        
                        ],
                    data=[
                        {'column1': 'Email','column2': 'yahoo.com','column3': emailcount.iloc[[0]].iloc[0] },
                        {'column1': 'Email','column2': 'gmail.com' ,'column3': emailcount.iloc[[1]].iloc[0]},
                        {'column1': 'Email','column2': 'hotmail.com' ,'column3': emailcount.iloc[[2]].iloc[0]},
                        {'column1': 'Email','column2': 'NA' ,'column3': emailcount.iloc[[3]].iloc[0]},
                        {'column1': 'Duplicate','column2': 'Phone numbers' ,'column3': str(len(df[df.duplicated(subset='phone',keep=False)])) + ' but all are NA.'},
                        {'column3': 'There are only 25 missing phone numbers with no duplicats. Greate way to get in contact with customer.'},
                        {'column1': 'Duplicate','column2': 'Emails' ,'column3': str(len(df[df.duplicated(subset='email',keep=False)])) + ' with ' + str(len(df[df.duplicated(subset='email',keep=False)]['email'].dropna())) + ' not NA.'},   
                        {'column3': 'Emails have many overlaps and thus is not a good way to get in contact with customers.'},
                        {'column1': 'Duplicate','column2': 'Work Email' ,'column3': str(len(df[df.duplicated(subset='work email',keep=False)])) + ' but all are NA.'},
                        {'column3': 'With respects to email, work email is much better than personal email.'},
                        {'column1': 'Duplicate','column2': 'Work phone numbers' ,'column3': str(len(df[df.duplicated(subset='work phone',keep=False)])) + ' but all are NA.'},                       
                        {'column3': 'Work phone number is essially as good as personal phone numbers.'},
                        {'column1': 'Missing', 'column2' : 'Name', 'column3' : 'There are ' + str(len(emptyname)) + ' rows with no name.'},
                        {'column3': 'These rows can be found in the readme.'},
                        
                    
                    ],
                    
                    page_action='none',
                    fixed_rows={'headers': True},
                    style_table={'height': '500px', 'overflowY': 'auto'},
                    style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white'},
                    style_data={'backgroundColor': 'rgb(50, 50, 50)','color': 'white'},
            ),
                
            ]    
     


#############################################################################
#creating call back for side bar
#############################################################################


    
    elif pathname == "/Account-Information":
        
        return [
            html.Div([
            html.H1(children='Choropleth Map'),

            html.Div(children=' This map is a distribution of the number of accounts '
                     + 'opened accross the country.'),
    
            dcc.Graph(
                id='Map',
                figure=mapfig
                ),
    
        
            html.H1(children='Line Chart'),

            html.Div(children=' The Line chart shows the number of accoutns opened '
                     +'from 1970-2017.'),
           
            
            
            dcc.Graph(
                id = 'example-graph0',
                figure = accounts,
                ),
                
   
    
             html.Div([ 
        
                html.Div([
                        html.Label("Top Cities Opening Accounts"),
                        dcc.Dropdown(
                            id = 'top',
                            options = [{'label': y, 'value': y }
                                       for y in list(range(1,101))
                                       ],
                            value =  5,
                            className = "dropdown",
                            ),
                        ]   
                    ),
   
                html.Div([
                dcc.Graph(
                id = 'horizontal-bar',
                figure = top_cities,
                ),

                    ]), 

            ]),
     ]),
    
                

]
    



#############################################################################
#creating call back for side bar
#############################################################################


    
@app.callback(
        Output(component_id='horizontal-bar', component_property='figure'),
        Input(component_id='top', component_property='value'), 
)
        
def update_hgraph(top): 
  
    

    dff3 = city_account_count.sort_values('Count',ascending=False)[:top].sort_values('Count',ascending=True)
    dff3 = dff3.fillna("No City Listed")
    
    hlinechart = px.bar(
        data_frame=dff3,
        x = 'Count',
        y = 'City',
        orientation = 'h'
        )

            

    hlinechart.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
     )
    


    return hlinechart






if __name__ == '__main__':
        app.run_server(host = '0.0.0.0', debug=True, port = 8060)                  
        


df.to_csv('/Users/koreynishimoto/Desktop/Takehome/newtakehome.csv')
