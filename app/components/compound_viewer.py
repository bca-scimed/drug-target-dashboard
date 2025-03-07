# components/compound_viewer.py

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
from io import BytesIO

# Import RDKit for molecular visualization
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem

class CompoundViewer:
    """
    Component for rendering molecular structures using RDKit.
    """
    def __init__(self, app):
        self.app = app
        self.register_callbacks()
    
    def render(self, id_prefix="compound-viewer"):
        """Render the compound viewer component."""
        return html.Div([
            dbc.Card([
                dbc.CardHeader("Compound Visualization"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                dbc.Label("SMILES String"),
                                dbc.Input(
                                    id=f"{id_prefix}-smiles-input",
                                    type="text",
                                    placeholder="Enter SMILES string...",
                                    value=""
                                ),
                                dbc.Button(
                                    "Render Structure",
                                    id=f"{id_prefix}-render-btn",
                                    color="primary",
                                    className="mt-2"
                                )
                            ])
                        ], md=6),
                        dbc.Col([
                            html.Div([
                                html.Img(id=f"{id_prefix}-structure-img", className="img-fluid")
                            ], className="text-center")
                        ], md=6)
                    ])
                ])
            ])
        ])
    
    def register_callbacks(self):
        """Register Dash callbacks for the component."""
        @self.app.callback(
            Output("compound-viewer-structure-img", "src"),
            [Input("compound-viewer-render-btn", "n_clicks")],
            [State("compound-viewer-smiles-input", "value")]
        )
        def render_molecule(n_clicks, smiles):
            if not n_clicks or not smiles:
                return ""
            
            try:
                # Parse SMILES and generate molecule
                mol = Chem.MolFromSmiles(smiles)
                if mol is None:
                    return ""
                
                # Add hydrogen atoms
                mol = Chem.AddHs(mol)
                
                # Generate 2D coordinates
                AllChem.Compute2DCoords(mol)
                
                # Create an image
                img = Draw.MolToImage(mol, size=(300, 300))
                
                # Convert image to base64 string for display
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                return f"data:image/png;base64,{img_str}"
            except Exception as e:
                print(f"Error rendering molecule: {e}")
                return ""

def create_compound_batch_viewer(compounds):
    """
    Create a grid of compound structures from a list of compounds.
    
    Args:
        compounds: List of compound objects with 'name' and 'smiles' attributes
    
    Returns:
        HTML Div containing a grid of compound structures
    """
    if not compounds:
        return html.Div("No compounds to display")
    
    # Filter compounds with valid SMILES
    valid_compounds = [c for c in compounds if c.smiles]
    
    if not valid_compounds:
        return html.Div("No valid SMILES strings to display")
    
    try:
        # Create molecule objects
        mols = []
        legends = []
        for compound in valid_compounds:
            mol = Chem.MolFromSmiles(compound.smiles)
            if mol:
                mols.append(mol)
                legends.append(compound.name)
        
        if not mols:
            return html.Div("Could not parse any valid molecules")
        
        # Generate a grid of images
        img = Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(200, 200), legends=legends)
        
        # Convert to base64 for display
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return html.Div([
            html.Img(src=f"data:image/png;base64,{img_str}", className="img-fluid")
        ], className="text-center mt-3")
    
    except Exception as e:
        print(f"Error rendering compound batch: {e}")
        return html.Div(f"Error rendering compounds: {str(e)}")