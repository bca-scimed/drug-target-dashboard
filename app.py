# app.py

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Import components
from app.components.compound_viewer import CompoundViewer, create_compound_batch_viewer
from app.components.structure_viewer import StructureViewer
from app.components.file_upload import FileUploadComponent
from app.components.relationship_manager import RelationshipManager

# Import database models and functions
from app.models.database import get_session, init_db
from app.models.targets import Target
from app.models.diseases import Disease
from app.models.compounds import Compound, CompoundActivity
from app.models.structures import Structure

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ],
    suppress_callback_exceptions=True
)

# Initialize the database
init_db()

# Initialize components
compound_viewer = CompoundViewer(app)
structure_viewer = StructureViewer(app)
file_upload = FileUploadComponent(app)
relationship_manager = RelationshipManager(app)

# Define the layout
app.layout = html.Div([
    dbc.NavbarSimple(
        brand="Drug Target Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    
    dbc.Container([
        dcc.Location(id='url', refresh=False),
        
        # Left sidebar
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Navigation"),
                    dbc.CardBody([
                        dbc.Nav([
                            dbc.NavLink("Dashboard", href="/", active="exact"),
                            dbc.NavLink("Targets", href="/targets", active="exact"),
                            dbc.NavLink("Diseases", href="/diseases", active="exact"),
                            dbc.NavLink("Compounds", href="/compounds", active="exact"),
                            dbc.NavLink("Structures", href="/structures", active="exact"),
                            dbc.NavLink("Relationships", href="/relationships", active="exact"),
                            dbc.NavLink("Import/Export", href="/import-export", active="exact")
                        ], vertical=True)
                    ])
                ]),
                
                html.Div(className="mt-4"),
                
                dbc.Card([
                    dbc.CardHeader("Quick Stats"),
                    dbc.CardBody([
                        html.Div(id="quick-stats")
                    ])
                ])
            ], md=3),
            
            # Main content area
            dbc.Col([
                html.Div(id="page-content")
            ], md=9)
        ])
    ], fluid=True)
])

# Define callback to update page content based on URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    """Render different content based on the URL pathname."""
    
    if pathname == "/" or pathname == "":
        # Dashboard page
        return html.Div([
            html.H2("Drug Target Dashboard"),
            html.Hr(),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Top Targets"),
                        dbc.CardBody([
                            html.Div(id="top-targets-list")
                        ])
                    ])
                ], md=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Recent Compounds"),
                        dbc.CardBody([
                            html.Div(id="recent-compounds-list")
                        ])
                    ])
                ], md=6)
            ]),
            
            html.Div(className="mt-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Featured Structure"),
                        dbc.CardBody([
                            html.Div(id="featured-structure")
                        ])
                    ])
                ], md=12)
            ])
        ])
    
    elif pathname == "/targets":
        # Targets page
        return html.Div([
            html.H2("Targets"),
            html.Hr(),
            
            dbc.Tabs([
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.Div(id="targets-list")
                ], label="Target List"),
                
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.H4("Add New Target"),
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Target Name *"),
                                dbc.Input(id="target-name-input", type="text", placeholder="Enter target name")
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Category"),
                                dbc.Input(id="target-category-input", type="text", placeholder="e.g., Kinase, GPCR")
                            ], md=6)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Validation Status"),
                                dbc.Select(
                                    id="target-validation-input",
                                    options=[
                                        {"label": "Validated", "value": "Validated"},
                                        {"label": "Emerging", "value": "Emerging"},
                                        {"label": "Putative", "value": "Putative"}
                                    ]
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Priority"),
                                dbc.Select(
                                    id="target-priority-input",
                                    options=[
                                        {"label": "High", "value": "High"},
                                        {"label": "Medium", "value": "Medium"},
                                        {"label": "Low", "value": "Low"}
                                    ]
                                )
                            ], md=6)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Description"),
                                dbc.Textarea(
                                    id="target-description-input",
                                    placeholder="Enter target description",
                                    style={"height": "150px"}
                                )
                            ], md=12)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Mechanism"),
                                dbc.Textarea(
                                    id="target-mechanism-input",
                                    placeholder="Enter target mechanism",
                                    style={"height": "150px"}
                                )
                            ], md=12)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Button("Add Target", id="add-target-btn", color="primary"),
                        html.Div(id="add-target-output", className="mt-3")
                    ])
                ], label="Add Target")
            ])
        ])
    
    elif pathname == "/diseases":
        # Diseases page
        return html.Div([
            html.H2("Diseases"),
            html.Hr(),
            
            dbc.Tabs([
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.Div(id="diseases-list")
                ], label="Disease List"),
                
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.H4("Add New Disease"),
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Disease Name *"),
                                dbc.Input(id="disease-name-input", type="text", placeholder="Enter disease name")
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Category"),
                                dbc.Input(id="disease-category-input", type="text", placeholder="e.g., Infectious, Neurological")
                            ], md=6)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Etiology"),
                                dbc.Textarea(
                                    id="disease-etiology-input",
                                    placeholder="Enter disease etiology",
                                    style={"height": "120px"}
                                )
                            ], md=12)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Prevalence"),
                                dbc.Input(id="disease-prevalence-input", type="text", placeholder="e.g., 1 in 1000")
                            ], md=12)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Treatment Landscape"),
                                dbc.Textarea(
                                    id="disease-treatment-input",
                                    placeholder="Enter treatment landscape",
                                    style={"height": "120px"}
                                )
                            ], md=12)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Button("Add Disease", id="add-disease-btn", color="primary"),
                        html.Div(id="add-disease-output", className="mt-3")
                    ])
                ], label="Add Disease")
            ])
        ])
    
    elif pathname == "/compounds":
        # Compounds page
        return html.Div([
            html.H2("Compounds"),
            html.Hr(),
            
            dbc.Tabs([
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.Div(id="compounds-list")
                ], label="Compound List"),
                
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.H4("Add New Compound"),
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Compound Name *"),
                                dbc.Input(id="compound-name-input", type="text", placeholder="Enter compound name")
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Molecular Formula"),
                                dbc.Input(id="compound-formula-input", type="text", placeholder="e.g., C9H8O4")
                            ], md=6)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("SMILES String"),
                                dbc.Input(id="compound-smiles-input", type="text", placeholder="Enter SMILES notation")
                            ], md=12)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Development Stage"),
                                dbc.Select(
                                    id="compound-stage-input",
                                    options=[
                                        {"label": "Discovery", "value": "Discovery"},
                                        {"label": "Preclinical", "value": "Preclinical"},
                                        {"label": "Phase I", "value": "Phase I"},
                                        {"label": "Phase II", "value": "Phase II"},
                                        {"label": "Phase III", "value": "Phase III"},
                                        {"label": "Approved", "value": "Approved"}
                                    ]
                                )
                            ], md=6)
                        ]),
                        
                        html.Div(className="mt-3"),
                        compound_viewer.render(),
                        
                        html.Div(className="mt-3"),
                        dbc.Button("Add Compound", id="add-compound-btn", color="primary"),
                        html.Div(id="add-compound-output", className="mt-3")
                    ])
                ], label="Add Compound")
            ])
        ])
    
    elif pathname == "/structures":
        # Structures page
        return html.Div([
            html.H2("Protein Structures"),
            html.Hr(),
            
            dbc.Tabs([
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.Div(id="structures-list")
                ], label="Structure List"),
                
                dbc.Tab([
                    html.Div(className="mt-3"),
                    html.H4("Add New Structure"),
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Target"),
                                dcc.Dropdown(
                                    id="structure-target-dropdown",
                                    options=relationship_manager._get_target_options(),
                                    placeholder="Select a target..."
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("PDB ID"),
                                dbc.Input(id="structure-pdb-id-input", type="text", placeholder="e.g., 1XYZ")
                            ], md=6)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Resolution (Å)"),
                                dbc.Input(id="structure-resolution-input", type="number", step="0.1", placeholder="e.g., 2.1")
                            ], md=6)
                        ]),
                        
                        html.Div(className="mt-3"),
                        dbc.Label("Upload PDB File"),
                        file_upload.render_upload(id_prefix="structure-pdb", upload_type="pdb"),
                        
                        html.Div(className="mt-3"),
                        dbc.Button("Add Structure", id="add-structure-btn", color="primary"),
                        html.Div(id="add-structure-output", className="mt-3")
                    ]),
                    
                    html.Div(className="mt-4"),
                    structure_viewer.render()
                ], label="Add Structure")
            ])
        ])
    
    elif pathname == "/relationships":
        # Relationships page
        return html.Div([
            html.H2("Relationship Management"),
            html.Hr(),
            
            dbc.Tabs([
                dbc.Tab([
                    html.Div(className="mt-3"),
                    relationship_manager.render_target_disease_manager()
                ], label="Target-Disease"),
                
                dbc.Tab([
                    html.Div(className="mt-3"),
                    relationship_manager.render_compound_activity_manager()
                ], label="Compound Activities")
            ])
        ])
    
    elif pathname == "/import-export":
        # Import/Export page
        return html.Div([
            html.H2("Data Import & Export"),
            html.Hr(),
            
            file_upload.render_data_import_export()
        ])
    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized...")
        ]
    )

# Define callback to update quick stats
@app.callback(
    Output("quick-stats", "children"),
    [Input("url", "pathname")]
)
def update_quick_stats(pathname):
    """Update the quick stats sidebar."""
    try:
        session = get_session()
        
        target_count = session.query(Target).count()
        disease_count = session.query(Disease).count()
        compound_count = session.query(Compound).count()
        structure_count = session.query(Structure).count()
        
        session.close()
        
        return html.Div([
            html.P([
                html.I(className="fas fa-crosshairs me-2"),
                f"Targets: {target_count}"
            ]),
            html.P([
                html.I(className="fas fa-disease me-2"),
                f"Diseases: {disease_count}"
            ]),
            html.P([
                html.I(className="fas fa-flask me-2"),
                f"Compounds: {compound_count}"
            ]),
            html.P([
                html.I(className="fas fa-cube me-2"),
                f"Structures: {structure_count}"
            ])
        ])
        
    except Exception as e:
        print(f"Error updating quick stats: {e}")
        return html.Div("Stats unavailable")

# Add callbacks for form submissions and data displays
# These would be added here for a complete application

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)