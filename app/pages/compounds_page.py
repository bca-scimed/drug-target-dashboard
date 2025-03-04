import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
from app.components.compound_form import create_compound_form
from app.models.compounds import Compound
from app.models.database import SessionLocal
import pandas as pd

def layout():
    return html.Div([
        # Main header and actions
        dbc.Row([
            dbc.Col(html.H2("Compounds"), width=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Add Compound", color="primary", id="btn-add-compound", n_clicks=0),
                    dbc.Button("Export", color="secondary", outline=True),
                ])
            ], width=4, className="text-end")
        ], className="page-header"),
        
        html.Hr(),
        
        # Main content layout
        dbc.Row([
            dbc.Col([
                html.Div(id="compounds-content")
            ])
        ]),
        
        # Compound table
        dbc.Row([
            dbc.Col([
                html.Div(id="compound-table-container", children=[
                    dash_table.DataTable(
                        id="compound-table",
                        columns=[
                            {"name": "Name", "id": "name"},
                            {"name": "Molecular Formula", "id": "molecular_formula"},
                            {"name": "Development Stage", "id": "development_stage"},
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
        create_compound_form(),
    ])

# Callback to open the modal
@callback(
    Output("compound-modal", "is_open"),
    [Input("btn-add-compound", "n_clicks"), Input("close-compound-modal", "n_clicks")],
    [State("compound-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback to save the compound
@callback(
    Output("compound-table", "data"),
    [Input("save-compound", "n_clicks")],
    [
        State("compound-name", "value"),
        State("compound-smiles", "value"),
        State("compound-formula", "value"),
        State("compound-stage", "value"),
        State("compound-table", "data"),
    ],
)
def save_compound(n_clicks, name, smiles, formula, stage, current_data):
    if n_clicks and name:
        # Save to database
        session = SessionLocal()
        new_compound = Compound(
            name=name,
            smiles=smiles,
            molecular_formula=formula,
            development_stage=stage
        )
        session.add(new_compound)
        session.commit()
        session.close()
        
        # Update table data
        return get_compound_data()
    
    return current_data or []

# Function to load compound data
def get_compound_data():
    session = SessionLocal()
    compounds = session.query(Compound).all()
    session.close()
    
    return [
        {
            "name": compound.name,
            "molecular_formula": compound.molecular_formula,
            "development_stage": compound.development_stage,
        }
        for compound in compounds
    ]

# Callback to load compound data on page load
@callback(
    Output("compound-table", "data", allow_duplicate=True),
    [Input("compounds-content", "children")],
    prevent_initial_call=True,
)
def load_compound_data(_):
    return get_compound_data()