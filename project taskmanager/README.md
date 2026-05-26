# Database Schema Designer
NAMES:
Saadi Abderrahim
Mimoune Islam
## Overview

This project is a Database Schema Designer desktop application developed using Python and PySide6.  
It allows users to visually design relational database schemas, manage tables and relationships, and automatically generate and execute SQL code.

The application strictly follows the Model–View–Controller (MVC) architectural pattern and respects usability principles defined by Scapin & Bastien.
## Features

### 1. Table Management
- Create tables with unique names
- Visual representation of tables as draggable blocks
- Rearrange tables freely on a canvas
- Delete tables safely without crashes

### 2. Relationship Management
- Create 1–N (one-to-many) relationships
- Create N–N (many-to-many) relationships
- Visual connectors between tables:
  - Solid line → 1–N
  - Dashed line → N–N
- Relationship lines update automatically when tables are moved

### 3. SQL Code Generation
- Automatic generation of valid CREATE TABLE SQL statements
- SQL displayed in a read-only panel
- Schema always synchronized with visual design

### 4. SQL Query Execution
- Execute generated SQL on an embedded SQLite database
- Safe execution with no crashes
- Immediate feedback to the user

---

## Architecture (MVC)

The application is structured using the Model–View–Controller pattern:

### Model
- Schema: stores tables and relationships
- Table: represents a database table
- Relationship: represents table relationships

### View
- Main window, dialogs, and canvas
- Visual elements only (no business logic)
- Drag & drop support

### Controller
- Handles user actions
- Connects Model and View
- Manages SQL generation and execution


---

## Project Structure


---

## Installation

### Requirements
- Python
- PySide6

Install dependencies:
`bash
pip install -r requirements.txt
