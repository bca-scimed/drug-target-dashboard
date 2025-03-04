import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State

def layout():
    return html.Div([
        # Main header and actions
        dbc.Row([
            dbc.Col(html.H2("Diseases"), width=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Add Disease", color="primary", id="btn-add-disease"),
                    dbc.Button("Export", color="secondary", outline=True),
                ])
            ], width=4, className="text-end")
        ], className="page-header"),
        
        html.Hr(),
        
        # Main content layout
        dbc.Row([
            dbc.Col([
                html.Div(id="diseases-content")
            ])
        ])
    ])