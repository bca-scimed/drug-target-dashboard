# components/relationship_manager.py

import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app.models.targets import Target
from app.models.diseases import Disease
from app.models.compounds import Compound, CompoundActivity
from app.models.database import get_session

class RelationshipManager:
    """Component for managing relationships between entities."""
    
    def __init__(self, app):
        self.app = app
        self.register_callbacks()
    
    def render_target_disease_manager(self):
        """Render the target-disease relationship management component."""
        return html.Div([
            dbc.Card([
                dbc.CardHeader("Target-Disease Relationships"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Select Target:"),
                            dcc.Dropdown(
                                id="target-disease-target-dropdown",
                                options=self._get_target_options(),
                                placeholder="Select a target..."
                            )
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Available Diseases:"),
                            dcc.Dropdown(
                                id="target-disease-disease-dropdown",
                                options=self._get_disease_options(),
                                placeholder="Select a disease...",
                                multi=True
                            )
                        ], md=6)
                    ]),
                    html.Div(className="mt-3"),
                    dbc.Button(
                        "Update Relationships",
                        id="target-disease-update-btn",
                        color="primary"
                    ),
                    html.Div(id="target-disease-update-output", className="mt-3"),
                    html.Div(className="mt-4"),
                    html.H5("Current Target-Disease Relationships"),
                    html.Div(id="target-disease-table-container")
                ])
            ])
        ])
    
    def render_compound_activity_manager(self):
        """Render the compound activity relationship management component."""
        return html.Div([
            dbc.Card([
                dbc.CardHeader("Compound Activity Data"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Select Compound:"),
                            dcc.Dropdown(
                                id="activity-compound-dropdown",
                                options=self._get_compound_options(),
                                placeholder="Select a compound..."
                            )
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Target:"),
                            dcc.Dropdown(
                                id="activity-target-dropdown",
                                options=self._get_target_options(),
                                placeholder="Select a target..."
                            )
                        ], md=6)
                    ]),
                    html.Div(className="mt-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Activity Type:"),
                            dbc.Input(
                                id="activity-type-input",
                                type="text",
                                placeholder="e.g., IC50, EC50, Ki"
                            )
                        ], md=4),
                        dbc.Col([
                            dbc.Label("Activity Value:"),
                            dbc.Input(
                                id="activity-value-input",
                                type="number",
                                placeholder="Enter value"
                            )
                        ], md=4),
                        dbc.Col([
                            dbc.Label("Unit:"),
                            dbc.Input(
                                id="activity-unit-input",
                                type="text",
                                placeholder="e.g., nM, μM"
                            )
                        ], md=4)
                    ]),
                    html.Div(className="mt-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Reference:"),
                            dbc.Input(
                                id="activity-reference-input",
                                type="text",
                                placeholder="Publication or reference"
                            )
                        ], md=12)
                    ]),
                    html.Div(className="mt-3"),
                    dbc.Button(
                        "Add Activity Data",
                        id="activity-add-btn",
                        color="primary"
                    ),
                    html.Div(id="activity-add-output", className="mt-3"),
                    html.Div(className="mt-4"),
                    html.H5("Current Compound Activity Data"),
                    html.Div(id="activity-table-container")
                ])
            ])
        ])
    
    def register_callbacks(self):
        """Register Dash callbacks for the relationship management components."""
        @self.app.callback(
            [Output("target-disease-update-output", "children"),
             Output("target-disease-table-container", "children")],
            [Input("target-disease-update-btn", "n_clicks")],
            [State("target-disease-target-dropdown", "value"),
             State("target-disease-disease-dropdown", "value")]
        )
        def update_target_disease_relationship(n_clicks, target_id, disease_ids):
            if not n_clicks or target_id is None:
                # Just display current relationships
                return None, self._render_target_disease_table()
            
            if disease_ids is None:
                disease_ids = []
            
            try:
                session = get_session()
                
                # Get the target
                target = session.query(Target).get(target_id)
                if not target:
                    return dbc.Alert("Target not found", color="danger"), self._render_target_disease_table()
                
                # Get the selected diseases
                selected_diseases = session.query(Disease).filter(Disease.id.in_(disease_ids)).all()
                
                # Update target's diseases
                target.diseases = selected_diseases
                
                # Commit changes
                session.commit()
                session.close()
                
                return dbc.Alert(
                    f"Successfully updated disease relationships for target: {target.name}",
                    color="success"
                ), self._render_target_disease_table()
                
            except Exception as e:
                print(f"Error updating target-disease relationships: {e}")
                return dbc.Alert(f"Error: {str(e)}", color="danger"), self._render_target_disease_table()
        
        @self.app.callback(
            [Output("activity-add-output", "children"),
             Output("activity-table-container", "children")],
            [Input("activity-add-btn", "n_clicks")],
            [State("activity-compound-dropdown", "value"),
             State("activity-target-dropdown", "value"),
             State("activity-type-input", "value"),
             State("activity-value-input", "value"),
             State("activity-unit-input", "value"),
             State("activity-reference-input", "value")]
        )
        def add_compound_activity(n_clicks, compound_id, target_id, activity_type, 
                                 activity_value, activity_unit, reference):
            if not n_clicks:
                # Just display current activities
                return None, self._render_activity_table()
            
            if compound_id is None or target_id is None:
                return dbc.Alert("Compound and Target are required", color="danger"), self._render_activity_table()
            
            try:
                session = get_session()
                
                # Create new activity
                new_activity = CompoundActivity(
                    compound_id=compound_id,
                    target_id=target_id,
                    activity_type=activity_type,
                    activity_value=activity_value,
                    activity_unit=activity_unit,
                    reference=reference
                )
                
                # Add to database
                session.add(new_activity)
                session.commit()
                
                # Get compound and target names for the alert
                compound_name = session.query(Compound).get(compound_id).name
                target_name = session.query(Target).get(target_id).name
                
                session.close()
                
                return dbc.Alert(
                    f"Successfully added activity data for {compound_name} against {target_name}",
                    color="success"
                ), self._render_activity_table()
                
            except Exception as e:
                print(f"Error adding compound activity: {e}")
                return dbc.Alert(f"Error: {str(e)}", color="danger"), self._render_activity_table()
    
    def _get_target_options(self):
        """Get dropdown options for targets."""
        try:
            session = get_session()
            targets = session.query(Target).all()
            options = [{"label": target.name, "value": target.id} for target in targets]
            session.close()
            return options
        except Exception as e:
            print(f"Error getting target options: {e}")
            return []
    
    def _get_disease_options(self):
        """Get dropdown options for diseases."""
        try:
            session = get_session()
            diseases = session.query(Disease).all()
            options = [{"label": disease.name, "value": disease.id} for disease in diseases]
            session.close()
            return options
        except Exception as e:
            print(f"Error getting disease options: {e}")
            return []
    
    def _get_compound_options(self):
        """Get dropdown options for compounds."""
        try:
            session = get_session()
            compounds = session.query(Compound).all()
            options = [{"label": compound.name, "value": compound.id} for compound in compounds]
            session.close()
            return options
        except Exception as e:
            print(f"Error getting compound options: {e}")
            return []
    
    def _render_target_disease_table(self):
        """Render a table of target-disease relationships."""
        try:
            session = get_session()
            
            # Get all targets with their diseases
            targets = session.query(Target).all()
            
            # Prepare data for the table
            data = []
            for target in targets:
                for disease in target.diseases:
                    data.append({
                        "target_id": target.id,
                        "target_name": target.name,
                        "disease_id": disease.id,
                        "disease_name": disease.name
                    })
            
            session.close()
            
            if not data:
                return html.Div("No target-disease relationships found")
            
            # Create a dash DataTable
            return dash_table.DataTable(
                data=data,
                columns=[
                    {"name": "Target", "id": "target_name"},
                    {"name": "Disease", "id": "disease_name"}
                ],
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "10px"
                },
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold"
                },
                page_size=10
            )
            
        except Exception as e:
            print(f"Error rendering target-disease table: {e}")
            return html.Div(f"Error loading data: {str(e)}")
    
    def _render_activity_table(self):
        """Render a table of compound activities."""
        try:
            session = get_session()
            
            # Get all compound activities with related data
            activities = session.query(CompoundActivity).all()
            
            # Prepare data for the table
            data = []
            for activity in activities:
                target = session.query(Target).get(activity.target_id)
                compound = session.query(Compound).get(activity.compound_id)
                
                if target and compound:
                    data.append({
                        "id": activity.id,
                        "compound_name": compound.name,
                        "target_name": target.name,
                        "activity_type": activity.activity_type or "N/A",
                        "activity_value": f"{activity.activity_value or 'N/A'} {activity.activity_unit or ''}",
                        "reference": activity.reference or "N/A"
                    })
            
            session.close()
            
            if not data:
                return html.Div("No compound activity data found")
            
            # Create a dash DataTable
            return dash_table.DataTable(
                data=data,
                columns=[
                    {"name": "Compound", "id": "compound_name"},
                    {"name": "Target", "id": "target_name"},
                    {"name": "Activity Type", "id": "activity_type"},
                    {"name": "Value", "id": "activity_value"},
                    {"name": "Reference", "id": "reference"}
                ],
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "10px"
                },
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold"
                },
                page_size=10
            )
            
        except Exception as e:
            print(f"Error rendering activity table: {e}")
            return html.Div(f"Error loading data: {str(e)}")