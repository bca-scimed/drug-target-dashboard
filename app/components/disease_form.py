import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback

def create_disease_form():
    """Create a modal form for adding or editing diseases"""
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Add New Disease")),
            dbc.ModalBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Disease Name", html_for="disease-name"),
                            dbc.Input(type="text", id="disease-name", placeholder="Enter disease name"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Category", html_for="disease-category"),
                            dbc.Select(
                                id="disease-category",
                                options=[
                                    {"label": "Viral", "value": "Viral"},
                                    {"label": "Bacterial", "value": "Bacterial"},
                                    {"label": "Fungal", "value": "Fungal"},
                                    {"label": "Parasitic", "value": "Parasitic"},
                                    {"label": "Neurological", "value": "Neurological"},
                                    {"label": "Cardiovascular", "value": "Cardiovascular"},
                                    {"label": "Respiratory", "value": "Respiratory"},
                                    {"label": "Metabolic", "value": "Metabolic"},
                                    {"label": "Genetic", "value": "Genetic"},
                                    {"label": "Other", "value": "Other"},
                                ],
                                placeholder="Select category",
                            ),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Etiology", html_for="disease-etiology"),
                            dbc.Textarea(
                                id="disease-etiology",
                                placeholder="Describe disease etiology/cause",
                                style={"height": "100px"},
                            ),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Prevalence", html_for="disease-prevalence"),
                            dbc.Input(type="text", id="disease-prevalence", placeholder="Enter disease prevalence"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Treatment Landscape", html_for="disease-treatment"),
                            dbc.Textarea(
                                id="disease-treatment",
                                placeholder="Describe current treatment options",
                                style={"height": "150px"},
                            ),
                        ], width=12),
                    ], className="mb-3"),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-disease-modal", className="ms-auto", n_clicks=0),
                dbc.Button("Save", id="save-disease", className="ms-2", color="primary", n_clicks=0),
            ]),
        ],
        id="disease-modal",
        size="lg",
        is_open=False,
    )