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
#from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df44 = pd.read_csv(r"data\clean_4x1_4x1.csv")
print("df44 imported")
df42 = pd.read_csv(r"data\clean_4x1_2x1.csv")
print("df42 imported")
df34 = pd.read_csv(r"data\clean_3x1_4x1.csv")
print("df34 imported")

# Sample dataframe for the example bar chart
df_chart = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Values": [4, 7, 1, 8]
})

print("sample chart created")
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

print("app created")

# Define the app layout
app.layout = dbc.Container([
    html.H1("45-Degree Modified Push-Off Test"),
    dcc.Tabs([
        dcc.Tab(label='Figures', children=[
            html.H2("Sample Bar Chart"),
            dcc.Graph(
                id='example-bar-chart',
                figure=px.bar(df_chart, x='Category', y='Values', title="Example Bar Chart")
            )
        ]),
        dcc.Tab(label='Raw Data', children=[
            html.H2("Data Tables"),
            dcc.Tabs([
                dcc.Tab(label='df44', children=[
                    dash_table.DataTable(
                        id='table-df44',
                        columns=[{"name": i, "id": i} for i in df44.columns],
                        data=df44.to_dict('records'),
                        page_size=10  # Display 10 rows per page
                    )
                ]),
                dcc.Tab(label='df42', children=[
                    dash_table.DataTable(
                        id='table-df42',
                        columns=[{"name": i, "id": i} for i in df42.columns],
                        data=df42.to_dict('records'),
                        page_size=10  # Display 10 rows per page
                    )
                ]),
                dcc.Tab(label='df34', children=[
                    dash_table.DataTable(
                        id='table-df34',
                        columns=[{"name": i, "id": i} for i in df34.columns],
                        data=df34.to_dict('records'),
                        page_size=10  # Display 10 rows per page
                    )
                ])
            ])
        ])
    ])
], fluid=True)

print("app layout complete")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
