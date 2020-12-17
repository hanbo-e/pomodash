#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 14:11:00 2020

@author: hanbo
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
#import base64


app = dash.Dash(__name__, title='my pomodoros')

#dense nightowl user data
my_path = 'data/data_0.txt'

#sparse narrow user data
#my_path = '/home/hanbo/Documents/stochastic-sage-student-code/pomodash/data/data_5.txt'

df = pd.read_csv(my_path, index_col=(0), parse_dates=(True))
df['month'] = df.index.month_name()
df['day'] = df.index.day_name()
df['hour'] = df.index.hour

#Summary stats for top panel of Dashboard
year = str(df.index.year[0])
grand_total = str(int(df['pomodoros'].sum()))
monthly_totals = df.groupby('month')['pomodoros'].sum()
peak_month = monthly_totals.nlargest(1)
peak_month

p_month = peak_month.index[0]
p_month_val = str(peak_month[0])

hourly_totals = df.groupby('hour')['pomodoros'].sum()
peak_hours = hourly_totals.nlargest(3)
peak_hours

#Total Pomodoros per topic for first chart
total_per_topic = pd.DataFrame(df[df['task'] != '0'].groupby('task')\
                               ['pomodoros'].sum())
total_per_topic.reset_index(inplace=True)
fig_total = px.bar(total_per_topic, x = 'task', y='pomodoros',
                   title=f'Total Pomodoros {year} per Task',
                   color="task")
fig_total.update_layout(
    font_color="#606060"
    )

#Monthly Pomodoros per topic for second chart
monthly_per_topic = pd.DataFrame(df[df['task'] != '0']\
                                 .groupby(['month','task'])\
                                     ['pomodoros'].sum())
monthly_per_topic.reset_index(inplace = True)
fig_monthly_per_topic = px.bar(monthly_per_topic, x = "task", y = "pomodoros",
                     title=f"Monthly Pomodoros {year} per Task",
                     color="task", 
                     facet_col=("month"),
                     facet_col_wrap=3, 
                     category_orders={"month": ["January",
                                                "February", "March", "April",
                                                "May", "June", "July", "August",
                                                "September", "October",
                                                "November", "December"]},
                     labels={'pomodoros':'pom'})
fig_monthly_per_topic.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig_monthly_per_topic.update_layout(
    font_color="#606060"
    )




by_day = df.resample(pd.Timedelta('1 day')).sum()
by_day['month'] = by_day.index.month_name()
by_day.drop(columns=['hour'], inplace=True)
fig_daily = px.bar(by_day, y="pomodoros", title="Daily Pomodoros per Month")

by_day = df.resample(pd.Timedelta('1 day')).sum()
by_day['month'] = by_day.index.month
by_day['month_name'] = by_day.index.month_name()
by_day.drop(columns=['hour'], inplace=True)

available_indicators = by_day['month_name'].unique()

################################################################

app.layout = html.Div(id='page-container', children=[
    
    html.Div(className="containerHeader", children=[
        html.Div(className="logoContainer",
                 children=[html.Img(className="myLogo", src='assets/my_pomo.png')]),
        
        html.Div(className="headerTitleContainer",
                 children=[
                     html.H2("My Pomodoro Dashboard")])       
        ]),
    #
    html.Div(className="summaryContainer", children=[
    #   
        html.Div(className="statsContainer",
                 children=[
                     html.Div(className="summaryValue",
                              children=[html.H1(f'{grand_total} pomodoros')]),
                     html.Div(className="summaryType",
                              children=[html.P(f'Total {year}')]),            
                     ]),
        #
        html.Div(className="statsContainer",
                 children=[
                     html.Div(className="summaryValue",
                              children=[html.H1(f'{str(int(peak_month[0]))} pomodoros')]),
                     html.Div(className="summaryType",
                              children=[html.P(f'Peak month | {peak_month.index[0]}')])
                     ]),
        html.Div(className="statsContainer",
                 children=[
                     html.Div(className="summaryValue",
                              children=[html.H1(f'{str(int(peak_hours[0]))} pomodoros')]),
                     html.Div(className="summaryType",
                              children=[html.P(f'Peak hour | {peak_hours.index[0]}:00')])
                     ])
        ]),
    
    html.Div(className="containerCharts",
             children=[
                 html.Div(className="topLeft chartsGeneralSettings", children=[dcc.Graph(
        id='total-graph',
        figure=fig_total)
                     ]),
                 html.Div(className="topRight chartsGeneralSettings", children=[    dcc.Graph(
        id='monthly-facet-graph',
        figure=fig_monthly_per_topic)]),
                 
                         
                 
                 html.Div(className="bottomLeft chartsGeneralSettings", children=[
                     
                     
                     
                     dcc.Graph(
        id='daily-per-month'),
                     
                     html.Div(className="controlLabel", children=[
                         "Select Month"
                         ]),
                     
                        html.Div([
            dcc.Dropdown(
                id='y-axis-option',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='January'
                )
            
            ], style={'width': '40%', 'display': 'inline-block', 'margin-left': '2%',
                      'color':'#FA4F56'}),
        
        
        
        
        ]),
                 
              
                 
 
#end of charts container
                 ])    
#end of page container
    ])
@app.callback(
    Output('daily-per-month', 'figure'),
    Input('y-axis-option', 'value'))
def update_graph(selected_month):
    dff = by_day[by_day['month_name'] == selected_month]
    fig = px.bar(dff, y='pomodoros', title="Daily Pomodoros per Month", labels={
        'index':'date'})
    fig.update_layout(transition_duration=500, font_color="#606060")
    fig.update_traces(marker_color="#FA4F56")

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)