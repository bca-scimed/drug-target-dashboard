import dash_bio as dashbio
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_structure_viewer(pdb_id=None, pdb_content=None):
    """Creates a 3D molecular structure viewer"""
    
    # Default empty state
    if not pdb_id and not pdb_content:
        return html.Div([
            html.H4("Protein Structure"),
            html.P("No structure selected", className="text-muted"),
            html.Div(className="empty-viewer")
        ], className="structure-viewer-container")
    
    # Create viewer with data
    return html.Div([
        html.H4("Protein Structure"),
        html.Div([
            html.Div([
                dbc.ButtonGroup([
                    dbc.Button("Cartoon", id="view-cartoon", color="primary", outline=True, size="sm"),
                    dbc.Button("Surface", id="view-surface", color="primary", outline=True, size="sm"),
                    dbc.Button("Stick", id="view-stick", color="primary", outline=True, size="sm"),
                ], className="mb-2"),
                dbc.ButtonGroup([
                    dbc.Button("Rainbow", id="color-rainbow", color="secondary", outline=True, size="sm"),
                    dbc.Button("Chain", id="color-chain", color="secondary", outline=True, size="sm"),
                    dbc.Button("Residue", id="color-residue", color="secondary", outline=True, size="sm"),
                ]),
            ], className="structure-controls"),
            
            dashbio.Molecule3dViewer(
                id='structure-viewer',
                modelData=pdb_content,
                styles={
                    'backgroundColor': 'white',
                    'height': '500px',
                },
                selectionType='atom',
            ) if pdb_content else 
            dashbio.Molecule3dViewer(
                id='structure-viewer',
                pdbId=pdb_id,
                styles={
                    'backgroundColor': 'white',
                    'height': '500px',
                },
                selectionType='atom',
            ),
            
            html.Div([
                html.Span(f"PDB ID: {pdb_id}" if pdb_id else "", className="pdb-id")
            ], className="structure-footer")
        ], className="structure-viewer-body")
    ], className="structure-viewer-container")