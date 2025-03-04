import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
from app.components.structure_form import create_structure_form
from app.models.targets import Structure, Target  # Updated this line
from app.models.database import SessionLocal
import pandas as pd

def layout():
    return html.Div([
        # Main header and actions
        dbc.Row([
            dbc.Col(html.H2("Structures"), width=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Add Structure", color="primary", id="btn-add-structure", n_clicks=0),
                    dbc.Button("Export", color="secondary", outline=True),
                ])
            ], width=4, className="text-end")
        ], className="page-header"),
        
        html.Hr(),
        
        # Main content layout
        dbc.Row([
            dbc.Col([
                html.Div(id="structures-content")
            ])
        ]),
        
        # Structure table
        dbc.Row([
            dbc.Col([
                html.Div(id="structure-table-container", children=[
                    dash_table.DataTable(
                        id="structure-table",
                        columns=[
                            {"name": "Target", "id": "target_name"},
                            {"name": "PDB ID", "id": "pdb_id"},
                            {"name": "Resolution (Å)", "id": "resolution"},
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
        create_structure_form(),
    ])

# Callback to open the modal
@callback(
    Output("structure-modal", "is_open"),
    [Input("btn-add-structure", "n_clicks"), Input("close-structure-modal", "n_clicks")],
    [State("structure-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback to save the structure
@callback(
    Output("structure-table", "data"),
    [Input("save-structure", "n_clicks")],
    [
        State("structure-target", "value"),
        State("structure-pdb-id", "value"),
        State("structure-resolution", "value"),
        State("structure-file-path", "value"),
        State("structure-table", "data"),
    ],
)
def save_structure(n_clicks, target_id, pdb_id, resolution, file_path, current_data):
    if n_clicks and target_id and pdb_id:
        # Save to database
        session = SessionLocal()
        new_structure = Structure(
            target_id=target_id,
            pdb_id=pdb_id,
            resolution=resolution,
            file_path=file_path
        )
        session.add(new_structure)
        session.commit()
        session.close()
        
        # Update table data
        return get_structure_data()
    
    return current_data or []

# Function to load structure data
def get_structure_data():
    session = SessionLocal()
    # Join with Target to get target names
    structures = session.query(
        Structure, Target.name.label("target_name")
    ).join(Target).all()
    session.close()
    
    return [
        {
            "target_name": structure[1],  # target_name from the join
            "pdb_id": structure[0].pdb_id,
            "resolution": structure[0].resolution,
        }
        for structure in structures
    ]

# Callback to load structure data on page load
@callback(
    Output("structure-table", "data", allow_duplicate=True),
    [Input("structures-content", "children")],
    prevent_initial_call=True,
)
def load_structure_data(_):
    return get_structure_data()