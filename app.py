import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State

from app.models import create_tables
from app.components.navbar import create_navbar
from app.pages.targets_page import layout as targets_layout
from app.pages.diseases_page import layout as diseases_layout
from app.pages.compounds_page import layout as compounds_layout
from app.pages.structures_page import layout as structures_layout

# Create tables if they don't exist
create_tables()

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)

# Define basic layout with left sidebar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    # Left sidebar
    dbc.Row([
        # Navigation sidebar
        dbc.Col(create_navbar(), width=2, className="sidebar"),
        
        # Main content area
        dbc.Col(html.Div(id='page-content'), width=10, className="content-wrapper")
    ], className="app-container")
])

# Page routing callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/diseases':
        return diseases_layout()  # Note the parentheses to call the function
    elif pathname == '/compounds':
        return compounds_layout()
    elif pathname == '/structures':
        return structures_layout()
    else:
        # Default to targets page
        return targets_layout()

if __name__ == '__main__':
    app.run_server(debug=True)