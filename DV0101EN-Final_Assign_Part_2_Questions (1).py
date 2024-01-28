#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
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
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
# year_list = [i for i in range(1980, 2013, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1: Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
   
    # TASK 2.2: Add two dropdown menus
    html.Label("Select Statistics:"),
    dcc.Dropdown(
        id='dropdown-statistics',
        options=dropdown_options,
        placeholder='Select a report type',
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),

    dcc.Dropdown(
        id='select-year',
        options=[{'label': str(i), 'value': i} for i in range(1980, 2014, 1)],
        placeholder='Select a year',
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
    ),

    # TASK 2.3: Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])

# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        

        
#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
         # grouping data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Plotting the line graph
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Year on year autombile sales during recessions"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        avg_vehicles_by_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_vehicles_by_type,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Number of Vehicles Sold by Vehicle Type over Recession Period'
            )
        )


# Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
            # grouping data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Expenditure Share by Vehicle Type during Recessions'
            )
        )

# Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales


        R_chart4 = dcc.Graph(
            figure=px.bar(
                recession_data,
                x='Vehicle_Type',
                y='Automobile_Sales',
                color='unemployment_rate',
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )
        
        # Return the plots in a 2x2 grid
        return [
        html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
        html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
]
    else:
        return []


# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    if selected_statistics == 'Yearly Statistics':
        # Filter the data for the selected year
        yearly_data = data[data['Year'] == selected_year]

                              
#TASK 2.5: Creating Graphs Yearly data
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales over the Whole Period'
            )
        )
            
# Plot 2 Total Monthly Automobile sales using line chart.
        total_monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                total_monthly_sales,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales for the Selected Year'
            )
        )

            # Plot bar chart for average number of vehicles sold during the given year
        avg_vehicles_by_type_yearly = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avg_vehicles_by_type_yearly,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)
            )
        )
        

            # Total Advertisement Expenditure for each vehicle using pie chart
        total_exp_by_vehicle = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                total_exp_by_vehicle,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle in {}'.format(selected_year)
            )
        )
        

#TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            html.Div(
                className='chart-item',
                children=[
                    html.Div(Y_chart1, style={'width': '50%'}),
                    html.Div(Y_chart2, style={'width': '50%'})
                ],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[
                    html.Div(Y_chart3),
                    html.Div(Y_chart4)
                ],
                style={'display': 'flex'}
            )
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)




