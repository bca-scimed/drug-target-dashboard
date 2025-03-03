import dash_bootstrap_components as dbc
from dash import html

def create_target_details(target=None):
    """Creates a panel displaying target details"""
    
    if not target:
        return html.Div([
            html.H4("Target Details"),
            html.P("No target selected", className="text-muted")
        ], className="target-details-container")
    
    return html.Div([
        # Target header
        html.Div([
            html.H4(target["name"], className="target-name"),
            html.Span(target["validation_status"], className=f"badge bg-{'success' if target['validation_status']=='established' else 'warning' if target['validation_status']=='partially_validated' else 'info'} me-2"),
            html.Span(target["priority"], className=f"badge bg-{'danger' if target['priority']=='high' else 'warning' if target['priority']=='medium' else 'secondary'}")
        ], className="target-header"),
        
        html.Hr(),
        
        # Target basic info
        dbc.Row([
            dbc.Col([
                html.Strong("Category:"),
                html.Span(target["category"], className="ms-2"),
            ], width=6, className="mb-2"),
            
            dbc.Col([
                html.Strong("Organism:"),
                html.Span(target["organism"], className="ms-2"),
            ], width=6, className="mb-2"),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Strong("Molecular Weight:"),
                html.Span(f"{target.get('molecular_weight', 'N/A')} kDa", className="ms-2"),
            ], width=6, className="mb-2"),
            
            dbc.Col([
                html.Strong("Cellular Location:"),
                html.Span(target.get("cellular_location", "N/A"), className="ms-2"),
            ], width=6, className="mb-2"),
        ]),
        
        html.Hr(),
        
        # Target description
        html.Div([
            html.H5("Description"),
            html.P(target["description"], className="target-description")
        ], className="mb-3"),
        
        # Target mechanism
        html.Div([
            html.H5("Mechanism"),
            html.P(target["mechanism"], className="target-mechanism")
        ], className="mb-3"),
        
        # Target alternative names
        html.Div([
            html.H5("Alternative Names"),
            html.P(target.get("alternative_names", "None"), className="target-alt-names")
        ], className="mb-3"),
        
        # Target notes
        html.Div([
            html.H5("Notes"),
            html.P(target.get("notes", "No additional notes"), className="target-notes")
        ], className="mb-3"),
        
        # Associated diseases section
        html.Div([
            html.H5("Associated Diseases"),
            html.Div(id="disease-list", className="disease-list")
        ], className="mb-3"),
        
    ], className="target-details-container")