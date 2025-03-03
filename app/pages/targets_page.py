import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State

def layout():
    return html.Div([
        # Main header and actions
        dbc.Row([
            dbc.Col(html.H2("Drug Targets"), width=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button("Add Target", color="primary", id="btn-add-target"),
                    dbc.Button("Export", color="secondary", outline=True),
                ])
            ], width=4, className="text-end")
        ], className="page-header"),
        
        html.Hr(),
        
        # Main content layout
        dbc.Row([
            # Left: Target list
            dbc.Col([
                # Search bar
                dbc.InputGroup([
                    dbc.Input(placeholder="Search targets...", id="target-search"),
                    dbc.InputGroupText(html.I(className="fas fa-search")),
                ], className="mb-3"),
                
                # Targets table
                dash_table.DataTable(
                    id="targets-table",
                    columns=[
                        {"name": "Name", "id": "name"},
                        {"name": "Category", "id": "category"},
                        {"name": "Validation", "id": "validation_status"},
                        {"name": "Priority", "id": "priority"},
                    ],
                    data=[],  # Will be populated from database
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left", "padding": "10px"},
                    style_header={
                        "backgroundColor": "var(--primary)",
                        "color": "white",
                        "fontWeight": "bold",
                    },
                    style_data_conditional=[{
                        "if": {"row_index": "odd"},
                        "backgroundColor": "var(--light-bg)"
                    }],
                    row_selectable="single",
                    page_size=10,
                ),
            ], width=4, className="target-list-col"),
            
            # Center: Structure viewer (when a target is selected)
            dbc.Col([
                html.Div(id="structure-viewer-container", className="structure-viewer-wrapper")
            ], width=4, className="structure-col"),
            
            # Right: Target details and info
            dbc.Col([
                html.Div(id="target-details-container", className="target-details-wrapper")
            ], width=4, className="details-col"),
        ], className="main-content-row"),
        
        # Bottom row for compounds
        dbc.Row([
            dbc.Col([
                html.Div(id="compounds-container", className="compounds-wrapper")
            ], width=12)
        ], className="compounds-row mt-4")
    ], className="page-container")