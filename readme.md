# Drug Target Dashboard
## Overview

The Drug Target Dashboard is a comprehensive web application for managing, visualizing, and analyzing drug targets and their associated compounds. This internal tool serves as a knowledge repository for early drug discovery projects, enabling scientists to quickly access and update information on potential therapeutic targets across various disease categories.
The dashboard is designed with a scientific focus, providing an intuitive interface to explore protein structures, review target validation status, and examine chemical compounds in a single integrated platform.

## Project Goals

- Create a centralized repository for drug target information across multiple therapeutic areas
- Provide detailed visualization of target structures in 3D
- Maintain comprehensive information on target validation status and disease associations
- Enable easy tracking of compounds associated with each target
- Support manual curation of all entries through both UI and direct database access
- Organize targets by priority, validation status, and therapeutic area

## Tools Used

- **PostgreSQL**: Relational database for storing all target and compound data
- **pgAdmin**: UI-based database management tool for direct data access and editing
- **Dash**: Python framework for building the interactive web application
- **SQLAlchemy**: ORM for database interaction from Python

## Key Libraries

- **dash-bootstrap-components**: For responsive, modern UI components
- **dash-bio**: For 3D molecular structure visualization
- **RDKit**: For chemical structure processing and 2D visualization
- **pandas**: For data manipulation and processing
- **psycopg2**: For PostgreSQL connection

## Features

- **Scientific UI Design**: Professional color scheme optimized for scientific/pharmaceutical applications
- **Left-side Navigation**: Easily switch between targets, diseases, compounds, and structures
- **Interactive Structure Viewer**: 3D visualization of protein structures with multiple rendering options
- **Compound Gallery**: 2D molecular structure display with key properties and activity data
- **Detailed Target Information**: Comprehensive view of target validation status, mechanism, and disease associations
- **Data Filtering**: Quick filters for target categories, validation status, and priority levels
- **Direct Database Access**: Full editing capabilities through pgAdmin for curated content
- **Manual Data Entry**: UI-based forms for adding and updating all information


## Usage
### Target Management

- Browse targets by category, validation status, or priority
- View detailed information about each target including mechanism and structural data
- Add/edit targets through the UI or directly via pgAdmin

### Structure Visualization

- Explore 3D protein structures in multiple visualization modes
- View binding sites and structural features
- Toggle between different rendering styles (cartoon, surface, stick)

### Compound Tracking

- Track compounds associated with each target
- View 2D molecular structures and key physicochemical properties
- Record and review activity data for each compound-target pair

### Specifications

- Designed for manual curation of 45-50 initial targets
- Focus on emerging infectious diseases and high-priority new therapeutic areas
- Supports SMILES structures for compounds with 2D molecular rendering
- Priority system for ranking targets by importance
- Validation status tracking (novel, partially validated, established)
- Scientific color palette with accessibility considerations


### Future Enhancements

- Integration with external structural databases
- Support for collaborative features and multi-user access
- Advanced similarity searching for compounds
- Integration with computational modeling tools
- Export capabilities for presentations and reporting