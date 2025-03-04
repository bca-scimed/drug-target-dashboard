import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
from app.components.disease_form import create_disease_form
from app.models.diseases import Disease
from app.models.database import SessionLocal
import pandas as pd

def layout():
    return html.Div([
        # Main header and actions
        dbc.Row([
            dbc.Col(html.H2("Diseases"), width=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Add Disease", color="primary", id="btn-add-disease", n_clicks=0),
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
        ]),
        
        # Disease table
        dbc.Row([
            dbc.Col([
                html.Div(id="disease-table-container", children=[
                    dash_table.DataTable(
                        id="disease-table",
                        columns=[
                            {"name": "Name", "id": "name"},
                            {"name": "Category", "id": "category"},
                            {"name": "Prevalence", "id": "prevalence"},
                        ],
                        data=[],
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "left",
                            "padding": "10px"
                        },
                        style_header={
                            "backgroundColor": "rgb(230, 230, 230)",
                            "fontWeight": "bold"
                        },
                        style_data_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "rgb(248, 248, 248)"
                            }
                        ],
                        page_size=10,
                        row_selectable="single",
                    )
                ])
            ])
        ], className="mt-4"),
        
        # Add the modal form
        create_disease_form(),
    ])

# Callback to open the modal
@callback(
    Output("disease-modal", "is_open"),
    [Input("btn-add-disease", "n_clicks"), Input("close-disease-modal", "n_clicks")],
    [State("disease-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback to save the disease
@callback(
    Output("disease-table", "data"),
    [Input("save-disease", "n_clicks")],
    [
        State("disease-name", "value"),
        State("disease-category", "value"),
        State("disease-etiology", "value"),
        State("disease-prevalence", "value"),
        State("disease-treatment", "value"),
        State("disease-table", "data"),
    ],
)
def save_disease(n_clicks, name, category, etiology, prevalence, treatment, current_data):
    if n_clicks and name:
        # Save to database
        session = SessionLocal()
        new_disease = Disease(
            name=name,
            category=category,
            etiology=etiology,
            prevalence=prevalence,
            treatment_landscape=treatment
        )
        session.add(new_disease)
        session.commit()
        session.close()
        
        # Update table data
        return get_disease_data()
    
    return current_data or []

# Function to load disease data
def get_disease_data():
    session = SessionLocal()
    diseases = session.query(Disease).all()
    session.close()
    
    return [
        {
            "name": disease.name,
            "category": disease.category,
            "prevalence": disease.prevalence,
        }
        for disease in diseases
    ]

# Callback to load disease data on page load
@callback(
    Output("disease-table", "data", allow_duplicate=True),
    [Input("diseases-content", "children")],
    prevent_initial_call=True,
)
def load_disease_data(_):
    return get_disease_data()