# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 00:55:28 2024

@author: Brian
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import pandas as pd

df44 = pd.read_csv(r"data\clean_4x1_4x1.csv")
print("df44 imported")
df42 = pd.read_csv(r"data\clean_4x1_2x1.csv")
print("df42 imported")
df34 = pd.read_csv(r"data\clean_3x1_4x1.csv")
print("df34 imported")
dataframes = {'df44': df44, 'df42': df42, 'df34': df34}


def df_arithmetic(df, col, func, const):
    #functions: 1:add, 2:subtract, 3:multiple, 4:divide
    name = 
    if(func==1):
        print("add")
        dataframes.df44["a"+c] =
    elif(func==2):
        print("sub")
    elif(func==3):
        print("mult")
    elif(func==4):
        print("div")
    




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

print("app created")

# Define the app layout
app.layout = dbc.Container([
    html.H1("45-Degree Modified Push-Off Test Data"),
    # Radio button selection for dataframe choice
    html.Label("Select Dataframe:"),
    dcc.RadioItems(
        id='dataframe-selector',
        options=[
            {'label': 'df44', 'value': 'df44'},
            {'label': 'df42', 'value': 'df42'},
            {'label': 'df34', 'value': 'df34'}
        ],
        value='df44',  # Default selection
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),
    
    # Row with x-axis checklist, y-axis checklist, and the figure
    dbc.Row([
        dbc.Col([
            html.Label("Select X-axis Column(s):"),
            dcc.Checklist(id='x-axis-checkbox', style={'display': 'flex', 'flex-direction': 'column'}),
        ], width=1),  # Fixed width for x-axis checklist
        
        dbc.Col([
            html.Label("Select Y-axis Column(s):"),
            dcc.Checklist(id='y-axis-checkbox', style={'display': 'flex', 'flex-direction': 'column'}),
        ], width=1),  # Fixed width for y-axis checklist
        
        dbc.Col([
            dcc.Graph(id='line-chart', style={'height': '670px', 'width': '100%'})  # Responsive width
        ], width='auto'),  # Dynamic width for figure column
    ]),
    
    # New row for displaying selected columns below the main row
    dbc.Row([
        dbc.Col([
            html.H4("Selected Columns"),
            html.Div(id='selected-columns', style={'margin-top': '10px'})  # Display selected columns here
        ])
    ], style={'margin-top': '20px'})  # Add margin to separate from the row above
], fluid=True)


# Callback to update checkbox options based on selected dataframe
@app.callback(
    [Output('x-axis-checkbox', 'options'),
     Output('y-axis-checkbox', 'options')],
    Input('dataframe-selector', 'value')
)
def update_axis_options(selected_df):
    # Get the columns of the selected dataframe
    df = dataframes[selected_df]
    columns = [{'label': col, 'value': col} for col in df.columns]
    
    # Add an option for using the index
    columns.insert(0, {'label': 'Index', 'value': 'index'})

    return columns, columns

# Callback to enforce the mutual exclusivity rule for x and y axes
@app.callback(
    [Output('x-axis-checkbox', 'value'),
     Output('y-axis-checkbox', 'value')],
    [Input('x-axis-checkbox', 'value'),
     Input('y-axis-checkbox', 'value')]
)
def enforce_exclusive_selection(x_selection, y_selection):
    # If more than one Y is selected, limit X to one selection and vice versa
    if len(y_selection) > 1:
        x_selection = x_selection[:1]  # Limit x-axis to a single selection
    if len(x_selection) > 1:
        y_selection = y_selection[:1]  # Limit y-axis to a single selection
    return x_selection, y_selection

# Callback to update the graph based on selected dataframe and axes
@app.callback(
    Output('line-chart', 'figure'),
    [Input('dataframe-selector', 'value'),
     Input('x-axis-checkbox', 'value'),
     Input('y-axis-checkbox', 'value')]
)
def update_line_chart(selected_df, x_axes, y_axes):
    df = dataframes[selected_df]

    # Handle cases where the index is selected as an axis
    if 'index' in x_axes:
        df = df.reset_index()
        x_axes = ['index']
    if 'index' in y_axes:
        df = df.reset_index()
        y_axes = [ax if ax != 'index' else 'index' for ax in y_axes]

    # Generate a line chart with multiple lines if multiple Y columns are selected
    if len(x_axes) == 1 and len(y_axes) >= 1:
        fig = px.line(df, x=x_axes[0], y=y_axes, title=f"{selected_df}: {x_axes[0]} vs {', '.join(y_axes)}")
    elif len(y_axes) == 1 and len(x_axes) >= 1:
        fig = px.line(df, x=x_axes, y=y_axes[0], title=f"{selected_df}: {', '.join(x_axes)} vs {y_axes[0]}")
    else:
        fig = px.line(title="Please select one x-axis and one or more y-axis, or vice versa")

    return fig

# Callback to display selected columns as toggleable buttons
@app.callback(
    Output('selected-columns', 'children'),
    [Input('x-axis-checkbox', 'value'),
     Input('y-axis-checkbox', 'value')]
)
def display_selected_columns(x_selection, y_selection):
    # Combine x and y selections
    selected_columns = set(x_selection + y_selection)
    selected_columns_list = list(selected_columns)
    
    # Create buttons for each selected column with toggle functionality
    buttons = [
        dbc.Button(
            col,
            id={'type': 'selected-column-button', 'index': col},
            color='primary',
            outline=True,
            style={'margin': '5px'}
        ) for col in selected_columns_list
    ]
    return buttons

# Callback to handle the toggling of buttons, ensuring only one is active at a time
@app.callback(
    Output({'type': 'selected-column-button', 'index': ALL}, 'color'),
    [Input({'type': 'selected-column-button', 'index': ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def toggle_buttons(n_clicks):
    # Identify which button was last clicked
    if not n_clicks:
        return ['primary'] * len(n_clicks)
    
    # Determine the index of the most recently clicked button
    active_button = None
    for i, n_click in enumerate(n_clicks):
        if n_click is not None and n_click > 0 and (active_button is None or n_click > n_clicks[active_button]):
            active_button = i

    # Set only the active button to "danger" and others to "primary"
    return ['danger' if i == active_button else 'primary' for i in range(len(n_clicks))]

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
