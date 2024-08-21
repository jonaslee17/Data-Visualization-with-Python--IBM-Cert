#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
# app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024)]

# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    
    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',  # Unique ID
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics'
        )
    ]),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='dropdown-year',  # Unique ID
            options=[{'label': i, 'value': i} for i in year_list],
            value=2024
        )
    ]),
    
    html.Div([  # TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'flex': '10px'})
    ])
])

# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('dropdown-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def disable_year(report_value):
    if report_value == "Recession":
    return True
    else:
    return False

def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

# Callback for plotting
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('dropdown-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # TASK 2.5: Create and display graphs for Recession Report Statistics
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation Over Recession Period")
        )
        
        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type")
        )
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, 
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title="Total Advertising Expenditure Share by Vehicle Type During Recessions")
        )
        
        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                x='Unemployment_Rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]
    
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # TASK 2.6: Create and display graphs for Yearly Report Statistics
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Average Automobile Sales')
        )
        
        # Plot 2: Total Monthly Automobile sales using line chart
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales')
        )
        
        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the Year {}'.format(input_year))
        )
        
        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title='Total Advertisement Expenditure for Each Vehicle Type in {}'.format(input_year))
        )
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]
    
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
