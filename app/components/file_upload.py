# components/file_upload.py

import os
import base64
import datetime
import json
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app.models.targets import Target
from app.models.diseases import Disease
from app.models.compounds import Compound
from app.models.structures import Structure
from app.models.database import get_session

class FileUploadComponent:
    """Component for file uploads and data import/export."""
    
    def __init__(self, app, upload_folder="uploads", allowed_extensions=None):
        self.app = app
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions or {
            'pdb': ['pdb'],
            'csv': ['csv'],
            'json': ['json'],
            'excel': ['xls', 'xlsx']
        }
        
        # Ensure upload directories exist
        os.makedirs(upload_folder, exist_ok=True)
        for subfolder in ['structures', 'imports', 'exports']:
            os.makedirs(os.path.join(upload_folder, subfolder), exist_ok=True)
        
        self.register_callbacks()
    
    def render_upload(self, id_prefix="file-upload", upload_type="pdb", accept=None):
        """
        Render a file upload component.
        
        Args:
            id_prefix: ID prefix for the component
            upload_type: Type of upload ('pdb', 'csv', 'json', 'excel')
            accept: Optional string of accepted file types
        """
        if accept is None:
            # Set default accept based on upload_type
            if upload_type in self.allowed_extensions:
                accept = ','.join([f'.{ext}' for ext in self.allowed_extensions[upload_type]])
        
        return html.Div([
            dbc.Card([
                dbc.CardHeader(f"Upload {upload_type.upper()} File"),
                dbc.CardBody([
                    dcc.Upload(
                        id=f"{id_prefix}-upload",
                        children=html.Div([
                            html.I(className="fas fa-file-upload me-2"),
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
                            'textAlign': 'center'
                        },
                        multiple=False,
                        accept=accept
                    ),
                    html.Div(id=f"{id_prefix}-output", className="mt-3"),
                    html.Div(id=f"{id_prefix}-filepath-store", style={"display": "none"})
                ])
            ])
        ])
    
    def render_data_import_export(self):
        """Render a component for data import and export."""
        return html.Div([
            dbc.Card([
                dbc.CardHeader("Data Import/Export"),
                dbc.CardBody([
                    dbc.Tabs([
                        dbc.Tab([
                            html.Div(className="mt-3"),
                            dbc.Form([
                                dbc.Label("Select data to import:"),
                                dbc.Select(
                                    id="import-data-type",
                                    options=[
                                        {"label": "Targets", "value": "targets"},
                                        {"label": "Diseases", "value": "diseases"},
                                        {"label": "Compounds", "value": "compounds"},
                                        {"label": "Structures", "value": "structures"},
                                        {"label": "Target-Disease Relationships", "value": "target_diseases"},
                                        {"label": "Compound Activities", "value": "compound_activities"}
                                    ],
                                    value="targets"
                                ),
                                html.Div(className="mb-3"),
                                self.render_upload(id_prefix="import-csv", upload_type="csv")
                            ])
                        ], label="Import"),
                        
                        dbc.Tab([
                            html.Div(className="mt-3"),
                            dbc.Form([
                                dbc.Label("Select data to export:"),
                                dbc.Select(
                                    id="export-data-type",
                                    options=[
                                        {"label": "Targets", "value": "targets"},
                                        {"label": "Diseases", "value": "diseases"},
                                        {"label": "Compounds", "value": "compounds"},
                                        {"label": "Structures", "value": "structures"},
                                        {"label": "Target-Disease Relationships", "value": "target_diseases"},
                                        {"label": "Compound Activities", "value": "compound_activities"}
                                    ],
                                    value="targets"
                                ),
                                html.Div(className="mt-3"),
                                dbc.Button("Export CSV", id="export-csv-btn", color="primary"),
                                html.Div(id="export-output", className="mt-3"),
                                dcc.Download(id="download-csv")
                            ])
                        ], label="Export")
                    ])
                ])
            ])
        ])
    
    def register_callbacks(self):
        """Register Dash callbacks for the components."""
        @self.app.callback(
            [Output("file-upload-output", "children"),
             Output("file-upload-filepath-store", "children")],
            [Input("file-upload-upload", "contents")],
            [State("file-upload-upload", "filename")]
        )
        def update_output(contents, filename):
            if contents is None:
                return None, None
            
            try:
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                
                # Validate file extension
                file_ext = filename.split('.')[-1].lower()
                valid_extension = False
                for ext_list in self.allowed_extensions.values():
                    if file_ext in ext_list:
                        valid_extension = True
                        break
                
                if not valid_extension:
                    return dbc.Alert(
                        f"Invalid file type: .{file_ext}. Please upload a valid file.",
                        color="danger"
                    ), None
                
                # Create unique filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                clean_filename = ''.join(c for c in filename if c.isalnum() or c in ['_', '.', '-'])
                subfolder = 'structures' if file_ext == 'pdb' else 'imports'
                filepath = os.path.join(self.upload_folder, subfolder, f"{timestamp}_{clean_filename}")
                
                # Save file
                with open(filepath, 'wb') as f:
                    f.write(decoded)
                
                return dbc.Alert(
                    [html.I(className="fas fa-check-circle me-2"), f"File uploaded: {filename}"],
                    color="success"
                ), filepath
            
            except Exception as e:
                print(f"Error uploading file: {e}")
                return dbc.Alert(
                    [html.I(className="fas fa-exclamation-circle me-2"), f"Error uploading file: {str(e)}"],
                    color="danger"
                ), None
        
        @self.app.callback(
            Output("import-csv-output", "children"),
            [Input("import-csv-upload", "contents")],
            [State("import-csv-upload", "filename"),
             State("import-data-type", "value")]
        )
        def import_data(contents, filename, data_type):
            if contents is None:
                return None
            
            try:
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                
                # Validate file extension
                file_ext = filename.split('.')[-1].lower()
                if file_ext not in self.allowed_extensions['csv']:
                    return dbc.Alert(
                        f"Invalid file type: .{file_ext}. Please upload a CSV file.",
                        color="danger"
                    )
                
                # Save file
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = os.path.join(self.upload_folder, 'imports', f"{timestamp}_{data_type}_{filename}")
                with open(filepath, 'wb') as f:
                    f.write(decoded)
                
                # Parse CSV
                df = pd.read_csv(filepath)
                rows_imported = len(df)
                
                # Here you would add logic to import data to the database
                # based on data_type and the contents of the CSV
                # For this example, we'll just acknowledge the import
                
                return dbc.Alert(
                    [
                        html.I(className="fas fa-check-circle me-2"),
                        f"Successfully imported {rows_imported} rows for {data_type}"
                    ],
                    color="success"
                )
            
            except Exception as e:
                print(f"Error importing data: {e}")
                return dbc.Alert(
                    [html.I(className="fas fa-exclamation-circle me-2"), f"Error importing data: {str(e)}"],
                    color="danger"
                )
        
        @self.app.callback(
            [Output("download-csv", "data"),
             Output("export-output", "children")],
            [Input("export-csv-btn", "n_clicks")],
            [State("export-data-type", "value")]
        )
        def export_data(n_clicks, data_type):
            if not n_clicks:
                return None, None
            
            try:
                # Here you would add logic to query database based on data_type
                # For this example, we'll generate dummy data
                
                from models.database import get_session, Target, Disease, Compound, Structure, CompoundActivity
                
                session = get_session()
                
                # Query database based on data_type
                if data_type == 'targets':
                    records = session.query(Target).all()
                    df = pd.DataFrame([{
                        'id': t.id,
                        'name': t.name,
                        'category': t.category,
                        'validation_status': t.validation_status,
                        'priority': t.priority,
                        'description': t.description,
                        'mechanism': t.mechanism
                    } for t in records])
                
                elif data_type == 'diseases':
                    records = session.query(Disease).all()
                    df = pd.DataFrame([{
                        'id': d.id,
                        'name': d.name,
                        'category': d.category,
                        'etiology': d.etiology,
                        'prevalence': d.prevalence,
                        'treatment_landscape': d.treatment_landscape
                    } for d in records])
                
                elif data_type == 'compounds':
                    records = session.query(Compound).all()
                    df = pd.DataFrame([{
                        'id': c.id,
                        'name': c.name,
                        'smiles': c.smiles,
                        'molecular_formula': c.molecular_formula,
                        'development_stage': c.development_stage
                    } for c in records])
                
                elif data_type == 'structures':
                    records = session.query(Structure).all()
                    df = pd.DataFrame([{
                        'id': s.id,
                        'target_id': s.target_id,
                        'pdb_id': s.pdb_id,
                        'resolution': s.resolution,
                        'file_path': s.file_path
                    } for s in records])
                
                else:
                    # Other data types
                    df = pd.DataFrame({'message': ['Export not implemented for this data type']})
                
                session.close()
                
                # Generate CSV
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{data_type}_{timestamp}.csv"
                
                return dict(
                    content=df.to_csv(index=False),
                    filename=filename
                ), dbc.Alert(
                    [html.I(className="fas fa-check-circle me-2"), f"Exported {len(df)} records to {filename}"],
                    color="success"
                )
            
            except Exception as e:
                print(f"Error exporting data: {e}")
                return None, dbc.Alert(
                    [html.I(className="fas fa-exclamation-circle me-2"), f"Error exporting data: {str(e)}"],
                    color="danger"
                )