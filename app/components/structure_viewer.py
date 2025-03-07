# components/structure_viewer.py

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_bio as dashbio
import os

class StructureViewer:
    """
    Component for visualizing 3D protein structures using dash-bio.
    """
    def __init__(self, app, upload_folder="uploads/structures"):
        self.app = app
        self.upload_folder = upload_folder
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
        
        self.register_callbacks()
    
    def render(self, id_prefix="structure-viewer", pdb_path=None, pdb_id=None):
        """
        Render the structure viewer component.
        
        Args:
            id_prefix: Prefix for component IDs
            pdb_path: Optional path to a local PDB file
            pdb_id: Optional PDB ID to fetch from RCSB
        """
        return html.Div([
            dbc.Card([
                dbc.CardHeader("Protein Structure Visualization"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                dbc.Label("PDB ID (from RCSB)"),
                                dbc.Input(
                                    id=f"{id_prefix}-pdb-id-input",
                                    type="text",
                                    placeholder="Enter PDB ID (e.g., 1AQ1)...",
                                    value=pdb_id or ""
                                ),
                                html.Div(className="mb-3"),
                                
                                dbc.Label("Or upload PDB file"),
                                dcc.Upload(
                                    id=f"{id_prefix}-upload",
                                    children=html.Div([
                                        'Drag and Drop or ',
                                        html.A('Select File')
                                    ]),
                                    style={
                                        'width': '100%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px 0'
                                    }
                                ),
                                
                                html.Div(id=f"{id_prefix}-upload-info"),
                                
                                dbc.Button(
                                    "Visualize Structure",
                                    id=f"{id_prefix}-visualize-btn",
                                    color="primary",
                                    className="mt-3"
                                )
                            ])
                        ], md=4),
                        dbc.Col([
                            html.Div(
                                id=f"{id_prefix}-mol3d-container",
                                style={"height": "500px", "width": "100%"}
                            )
                        ], md=8)
                    ])
                ])
            ])
        ])
    
    def register_callbacks(self):
        """Register Dash callbacks for the component."""
        @self.app.callback(
            [Output("structure-viewer-mol3d-container", "children"),
             Output("structure-viewer-upload-info", "children")],
            [Input("structure-viewer-visualize-btn", "n_clicks"),
             Input("structure-viewer-upload", "contents")],
            [State("structure-viewer-upload", "filename"),
             State("structure-viewer-pdb-id-input", "value")]
        )
        def update_output(n_clicks, contents, filename, pdb_id):
            ctx = dash.callback_context
            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
            
            # Default return values
            viewer = html.Div("No structure loaded yet")
            upload_info = ""
            
            if not ctx.triggered:
                return viewer, upload_info
                
            try:
                if trigger_id == "structure-viewer-upload" and contents:
                    # Handle file upload
                    import base64
                    import datetime
                    
                    content_type, content_string = contents.split(',')
                    decoded = base64.b64decode(content_string)
                    
                    # Create a unique filename
                    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    clean_filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '.', '-'])
                    filepath = os.path.join(self.upload_folder, f"{now}_{clean_filename}")
                    
                    # Save file
                    with open(filepath, 'wb') as f:
                        f.write(decoded)
                    
                    upload_info = dbc.Alert(f"File uploaded: {filename}", color="success")
                    
                    # Create viewer
                    viewer = dashbio.Molecule3dViewer(
                        id='molecule-3d',
                        modelData=self._parse_pdb_file(filepath),
                        styles={
                            'sphere': {
                                'sphere': {
                                    'hidden': True
                                }
                            }
                        },
                        backgroundColor="#FFFFFF",
                        height=500
                    )
                    
                elif trigger_id == "structure-viewer-visualize-btn" and pdb_id:
                    # Use PDB ID from RCSB
                    viewer = dashbio.Molecule3dViewer(
                        id='molecule-3d',
                        pdbId=pdb_id,
                        styles={
                            'sphere': {
                                'sphere': {
                                    'hidden': True
                                }
                            }
                        },
                        backgroundColor="#FFFFFF",
                        height=500
                    )
                    
                    upload_info = dbc.Alert(f"Loaded PDB: {pdb_id}", color="success")
            
            except Exception as e:
                print(f"Error in structure viewer: {e}")
                viewer = html.Div("Error loading structure")
                upload_info = dbc.Alert(f"Error: {str(e)}", color="danger")
            
            return viewer, upload_info
    
    def _parse_pdb_file(self, filepath):
        """Parse a PDB file for the Molecule3dViewer."""
        # This is a simplified parser - in a production app,
        # you might want to use a more robust PDB parser
        try:
            with open(filepath, 'r') as f:
                pdb_string = f.read()
            
            # Parse the PDB data into the format expected by Molecule3dViewer
            # This is a very simplified version - a real implementation would be more robust
            atoms = []
            bonds = []
            
            atom_index = {}  # Map from PDB atom index to our index
            idx = 0
            
            for line in pdb_string.split('\n'):
                if line.startswith('ATOM') or line.startswith('HETATM'):
                    # Parse atom information
                    atom_serial = int(line[6:11].strip())
                    atom_name = line[12:16].strip()
                    residue_name = line[17:20].strip()
                    chain_id = line[21:22].strip()
                    residue_seq = int(line[22:26].strip())
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    
                    # Element symbol (columns 77-78)
                    if len(line) >= 78:
                        element = line[76:78].strip()
                    else:
                        # Extract from atom name
                        element = atom_name[0]
                    
                    # Add atom to the list
                    atoms.append({
                        'serial': atom_serial,
                        'name': atom_name,
                        'residue_name': residue_name,
                        'chain_id': chain_id,
                        'residue_index': residue_seq,
                        'positions': [x, y, z],
                        'atom_type': element
                    })
                    
                    atom_index[atom_serial] = idx
                    idx += 1
                
                elif line.startswith('CONECT'):
                    # Parse bond information
                    fields = line.split()
                    if len(fields) > 2:
                        atom1 = int(fields[1])
                        for i in range(2, len(fields)):
                            atom2 = int(fields[i])
                            if atom1 in atom_index and atom2 in atom_index:
                                bonds.append([atom_index[atom1], atom_index[atom2]])
            
            return {
                'atoms': atoms,
                'bonds': bonds
            }
            
        except Exception as e:
            print(f"Error parsing PDB file: {e}")
            return {'atoms': [], 'bonds': []}