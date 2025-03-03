import dash_bootstrap_components as dbc
from dash import html

def create_navbar():
    return html.Div([
        # Logo and title
        html.Div([
            html.Img(src='/assets/logo.png', height='50px', className="mb-3"),
            html.H3("Drug Target Explorer", className="navbar-title")
        ], className="navbar-header"),
        
        html.Hr(),
        
        # Navigation links
        dbc.Nav([
            dbc.NavLink([html.I(className="fas fa-bullseye me-2"), "Targets"], href="/", active="exact", className="nav-link"),
            dbc.NavLink([html.I(className="fas fa-disease me-2"), "Diseases"], href="/diseases", active="exact", className="nav-link"),
            dbc.NavLink([html.I(className="fas fa-pills me-2"), "Compounds"], href="/compounds", active="exact", className="nav-link"),
            dbc.NavLink([html.I(className="fas fa-cube me-2"), "Structures"], href="/structures", active="exact", className="nav-link"),
        ], vertical=True, pills=True, className="nav-links"),
        
        html.Hr(),
        
        # Quick filters section
        html.Div([
            html.H5("Quick Filters"),
            dbc.Label("Categories:"),
            dbc.Checklist(
                options=[
                    {"label": "Cardiovascular", "value": "cardiovascular"},
                    {"label": "Viral", "value": "viral"},
                    {"label": "Fungal", "value": "fungal"},
                    {"label": "Metabolic", "value": "metabolic"},
                ],
                id="category-filter",
                className="filter-list"
            ),
            
            html.Br(),
            
            dbc.Label("Validation:"),
            dbc.Checklist(
                options=[
                    {"label": "Established", "value": "established"},
                    {"label": "Partially Validated", "value": "partially_validated"},
                    {"label": "Novel", "value": "novel"},
                ],
                id="validation-filter",
                className="filter-list"
            ),
            
            html.Br(),
            
            dbc.Label("Priority:"),
            dbc.RadioItems(
                options=[
                    {"label": "All", "value": "all"},
                    {"label": "High", "value": "high"},
                    {"label": "Medium", "value": "medium"},
                    {"label": "Low", "value": "low"},
                ],
                id="priority-filter",
                value="all",
                className="filter-list"
            ),
        ], className="filter-section")
    ], className="sidebar-content")