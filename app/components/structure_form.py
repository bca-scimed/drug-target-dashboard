import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback
from app.models.targets import Target
from app.models.database import SessionLocal

def create_structure_form():
    """Create a modal form for adding or editing structures"""
    
    # Get all targets to populate the dropdown
    session = SessionLocal()
    targets = session.query(Target).all()
    session.close()
    
    target_options = [{"label": target.name, "value": target.id} for target in targets]
    
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Add New Structure")),
            dbc.ModalBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Target", html_for="structure-target"),
                            dbc.Select(
                                id="structure-target",
                                options=target_options,
                                placeholder="Select target",
                            ),
                            dbc.FormText("Select the target this structure belongs to"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("PDB ID", html_for="structure-pdb-id"),
                            dbc.Input(type="text", id="structure-pdb-id", placeholder="e.g., 6LU7"),
                            dbc.FormText("Enter the Protein Data Bank ID"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Resolution (Å)", html_for="structure-resolution"),
                            dbc.Input(type="number", id="structure-resolution", placeholder="e.g., 2.16", step=0.01),
                        ], width=12),
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("File Path", html_for="structure-file-path"),
                            dbc.Input(type="text", id="structure-file-path", placeholder="/assets/structures/filename.pdb"),
                            dbc.FormText("Enter the path to the PDB file"),
                        ], width=12),
                    ], className="mb-3"),
                    
                    # We'll add file upload functionality later
                    dbc.Row([
                        dbc.Col([
                            html.P("File upload functionality will be added in a future update.", className="text-muted"),
                        ], width=12),
                    ], className="mb-3"),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-structure-modal", className="ms-auto", n_clicks=0),
                dbc.Button("Save", id="save-structure", className="ms-2", color="primary", n_clicks=0),
            ]),
        ],
        id="structure-modal",
        size="lg",
        is_open=False,
    )

# Add this callback to refresh target options
@callback(
    Output("structure-target", "options"),
    [Input("btn-add-structure", "n_clicks")],
)
def refresh_target_options(n_clicks):
    if n_clicks:
        session = SessionLocal()
        targets = session.query(Target).all()
        session.close()
        return [{"label": target.name, "value": target.id} for target in targets]
    # Initial options
    session = SessionLocal()
    targets = session.query(Target).all()
    session.close()
    return [{"label": target.name, "value": target.id} for target in targets]