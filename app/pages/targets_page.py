import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
from app.components.target_form import create_target_form
from app.models.targets import Target
from app.models.database import SessionLocal
import pandas as pd

def layout():
    return html.Div([
        # Main header and actions
        dbc.Row([
            dbc.Col(html.H2("Drug Targets"), width=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Add Target", color="primary", id="btn-add-target", n_clicks=0),
                    dbc.Button("Export", color="secondary", outline=True),
                ])
            ], width=4, className="text-end")
        ], className="page-header"),
        
        html.Hr(),
        
        # Main content layout
        dbc.Row([
            dbc.Col([
                html.Div(id="targets-content")
            ])
        ]),
        
        # Target table
        dbc.Row([
            dbc.Col([
                html.Div(id="target-table-container", children=[
                    dash_table.DataTable(
                        id="target-table",
                        columns=[
                            {"name": "Name", "id": "name"},
                            {"name": "Category", "id": "category"},
                            {"name": "Validation", "id": "validation_status"},
                            {"name": "Priority", "id": "priority"},
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
        create_target_form(),
    ])

# Callback to open the modal
@callback(
    Output("target-modal", "is_open"),
    [Input("btn-add-target", "n_clicks"), Input("close-target-modal", "n_clicks")],
    [State("target-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback to save the target
@callback(
    Output("target-table", "data"),
    [Input("save-target", "n_clicks")],
    [
        State("target-name", "value"),
        State("target-category", "value"),
        State("target-validation", "value"),
        State("target-priority", "value"),
        State("target-mechanism", "value"),
        State("target-description", "value"),
        State("target-table", "data"),
    ],
)
def save_target(n_clicks, name, category, validation, priority, mechanism, description, current_data):
    if n_clicks and name:
        # Save to database
        session = SessionLocal()
        new_target = Target(
            name=name,
            category=category,
            validation_status=validation,
            priority=priority,
            mechanism=mechanism,
            description=description
        )
        session.add(new_target)
        session.commit()
        session.close()
        
        # Update table data
        return get_target_data()
    
    return current_data or []

# Function to load target data
def get_target_data():
    session = SessionLocal()
    targets = session.query(Target).all()
    session.close()
    
    return [
        {
            "name": target.name,
            "category": target.category,
            "validation_status": target.validation_status,
            "priority": target.priority,
        }
        for target in targets
    ]

# Callback to load target data on page load
@callback(
    Output("target-table", "data", allow_duplicate=True),
    [Input("targets-content", "children")],
    prevent_initial_call=True,
)
def load_target_data(_):
    return get_target_data()