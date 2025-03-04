import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback

def create_compound_form():
    """Create a modal form for adding or editing compounds"""
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Add New Compound")),
            dbc.ModalBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Compound Name", html_for="compound-name"),
                            dbc.Input(type="text", id="compound-name", placeholder="Enter compound name"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("SMILES", html_for="compound-smiles"),
                            dbc.Textarea(
                                id="compound-smiles",
                                placeholder="Enter SMILES notation",
                                style={"height": "100px"},
                            ),
                            dbc.FormText("Enter the chemical structure in SMILES format"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Molecular Formula", html_for="compound-formula"),
                            dbc.Input(type="text", id="compound-formula", placeholder="e.g., C21H30O2"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Development Stage", html_for="compound-stage"),
                            dbc.Select(
                                id="compound-stage",
                                options=[
                                    {"label": "Discovery", "value": "Discovery"},
                                    {"label": "Preclinical", "value": "Preclinical"},
                                    {"label": "Phase I", "value": "Phase I"},
                                    {"label": "Phase II", "value": "Phase II"},
                                    {"label": "Phase III", "value": "Phase III"},
                                    {"label": "Approved", "value": "Approved"},
                                    {"label": "Withdrawn", "value": "Withdrawn"},
                                ],
                                placeholder="Select development stage",
                            ),
                        ], width=12),
                    ], className="mb-3"),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-compound-modal", className="ms-auto", n_clicks=0),
                dbc.Button("Save", id="save-compound", className="ms-2", color="primary", n_clicks=0),
            ]),
        ],
        id="compound-modal",
        size="lg",
        is_open=False,
    )