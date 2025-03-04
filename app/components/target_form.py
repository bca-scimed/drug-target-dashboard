import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback

def create_target_form():
    """Create a modal form for adding or editing targets"""
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Add New Target")),
            dbc.ModalBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Target Name", html_for="target-name"),
                            dbc.Input(type="text", id="target-name", placeholder="Enter target name"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Category", html_for="target-category"),
                            dbc.Select(
                                id="target-category",
                                options=[
                                    {"label": "Enzyme", "value": "Enzyme"},
                                    {"label": "Receptor", "value": "Receptor"},
                                    {"label": "Ion Channel", "value": "Ion Channel"},
                                    {"label": "Transporter", "value": "Transporter"},
                                    {"label": "Viral Protease", "value": "Viral Protease"},
                                    {"label": "Other", "value": "Other"},
                                ],
                                placeholder="Select category",
                            ),
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Validation Status", html_for="target-validation"),
                            dbc.Select(
                                id="target-validation",
                                options=[
                                    {"label": "Validated", "value": "Validated"},
                                    {"label": "Emerging", "value": "Emerging"},
                                    {"label": "Potential", "value": "Potential"},
                                    {"label": "Unvalidated", "value": "Unvalidated"},
                                ],
                                placeholder="Select validation status",
                            ),
                        ], width=6),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Priority", html_for="target-priority"),
                            dbc.Select(
                                id="target-priority",
                                options=[
                                    {"label": "High", "value": "High"},
                                    {"label": "Medium", "value": "Medium"},
                                    {"label": "Low", "value": "Low"},
                                ],
                                placeholder="Select priority",
                            ),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Mechanism", html_for="target-mechanism"),
                            dbc.Textarea(
                                id="target-mechanism",
                                placeholder="Describe target mechanism of action",
                                style={"height": "100px"},
                            ),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Description", html_for="target-description"),
                            dbc.Textarea(
                                id="target-description",
                                placeholder="Enter detailed description",
                                style={"height": "150px"},
                            ),
                        ], width=12),
                    ], className="mb-3"),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-target-modal", className="ms-auto", n_clicks=0),
                dbc.Button("Save", id="save-target", className="ms-2", color="primary", n_clicks=0),
            ]),
        ],
        id="target-modal",
        size="lg",
        is_open=False,
    )