from dash import html, dcc
import dash_bootstrap_components as dbc
import base64
from rdkit import Chem
from rdkit.Chem import Draw
import io

def create_compound_card(compound):
    """Creates a card displaying compound information and structure"""
    
    # Generate 2D structure from SMILES
    mol = Chem.MolFromSmiles(compound["smiles"])
    img = Draw.MolToImage(mol, size=(200, 200))
    
    # Convert image to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return dbc.Card([
        dbc.Row([
            # Image on the left
            dbc.Col(
                html.Img(src=f"data:image/png;base64,{img_str}", className="compound-structure"),
                width=4
            ),
            # Details on the right
            dbc.Col([
                html.H5(compound["name"], className="compound-name"),
                html.P(f"MW: {compound['molecular_weight']:.2f} | LogP: {compound['logp']:.2f}", className="compound-props"),
                html.P(f"Stage: {compound['development_stage']}", className="compound-stage"),
                html.P(f"Activity: {compound['activity_value']} {compound['activity_unit']} ({compound['activity_type']})", className="compound-activity"),
            ], width=8)
        ]),
        dbc.CardFooter(
            dbc.Button("View Details", size="sm", color="primary", outline=True),
            className="text-end"
        )
    ], className="compound-card mb-3")

def create_compounds_section(compounds):
    """Creates a section displaying compound cards and summary info"""
    
    if not compounds:
        return html.Div([
            html.H4("Related Compounds"),
            html.P("No compounds associated with this target", className="text-muted")
        ], className="compounds-container")
    
    return html.Div([
        html.H4("Related Compounds"),
        html.Div([
            dbc.Row([
                dbc.Col(
                    create_compound_card(compound),
                    width=6
                ) for compound in compounds
            ])
        ], className="compounds-list")
    ], className="compounds-container")