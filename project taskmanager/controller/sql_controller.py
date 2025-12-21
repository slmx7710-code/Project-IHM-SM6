import sqlite3
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
import re

class SQLController:
    def __init__(self, window):
        self.window = window
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        self.window.ui.executeQueryButton.clicked.connect(self.execute_query)

    def load_schema(self, sql_code):
        try:
            self.cursor.executescript(sql_code)
            self.conn.commit()
        except Exception:
            pass

    def execute_query(self):
        query = self.window.ui.queryInput.toPlainText().strip()
        if not query:
            QMessageBox.warning(self.window, "Warning", "Please enter an SQL query")
            return

        try:
            # Check if it's a CREATE TABLE query
            if query.strip().upper().startswith("CREATE TABLE"):
                # Extract table name from SQL
                table_name = self.extract_table_name(query)
                
                # Execute the query
                self.cursor.execute(query)
                self.conn.commit()
                
                # Try to add table to canvas
                self.add_table_to_canvas_from_sql(query, table_name)
                
                QMessageBox.information(self.window, "Success", f"Table '{table_name}' created and added to canvas")
                
                # Show message in result table
                table = self.window.ui.resultTable
                table.setRowCount(1)
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels(["Action", "Result"])
                table.setItem(0, 0, QTableWidgetItem("Table Created"))
                table.setItem(0, 1, QTableWidgetItem(f"Table '{table_name}' added to canvas"))
                table.setVisible(True)
                
            elif query.strip().upper().startswith("SELECT"):
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                cols = [d[0] for d in self.cursor.description]

                table = self.window.ui.resultTable
                table.setRowCount(len(rows))
                table.setColumnCount(len(cols))
                table.setHorizontalHeaderLabels(cols)
                table.setVisible(True)

                for r, row in enumerate(rows):
                    for c, value in enumerate(row):
                        table.setItem(r, c, QTableWidgetItem(str(value)))
                
                QMessageBox.information(self.window, "Success", f"Query executed! {len(rows)} rows displayed")
            else:
                self.cursor.execute(query)
                self.conn.commit()
                rows_affected = self.cursor.rowcount
                
                table = self.window.ui.resultTable
                table.setRowCount(1)
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels(["Action", "Result"])
                table.setItem(0, 0, QTableWidgetItem("Executed"))
                table.setItem(0, 1, QTableWidgetItem(f"{rows_affected} rows affected"))
                table.setVisible(True)
                
                QMessageBox.information(self.window, "Success", f"Query executed! {rows_affected} rows affected")

        except Exception as e:
            QMessageBox.critical(self.window, "SQL Error", str(e))
            
            table = self.window.ui.resultTable
            table.setRowCount(1)
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Type", "Message"])
            table.setItem(0, 0, QTableWidgetItem("Error"))
            table.setItem(0, 1, QTableWidgetItem(str(e)))
            table.setVisible(True)

    def extract_table_name(self, sql):
        """Extract table name from CREATE TABLE statement"""
        # Simple regex to extract table name
        match = re.search(r'CREATE TABLE (\w+)', sql, re.IGNORECASE)
        if match:
            return match.group(1)
        return "unknown_table"

    def add_table_to_canvas_from_sql(self, sql, table_name):
        """Parse SQL and add table to canvas"""
        try:
            # Parse columns from SQL
            columns = self.parse_columns_from_sql(sql)
            
            # Add table to schema model
            if hasattr(self.window, 'controller'):
                controller = self.window.controller
                
                # Check if table already exists
                existing_tables = [t.name for t in controller.schema.tables]
                if table_name in existing_tables:
                    print(f"Table '{table_name}' already exists in schema")
                    return
                
                # Create new table
                from model.table_model import Table, Attribute
                table = Table(table_name)
                
                # Add attributes
                for col in columns:
                    attr = Attribute(
                        name=col['name'],
                        data_type=col['type'],
                        primary_key=col.get('primary_key', False)
                    )
                    table.add_attribute(attr)
                
                # Add table to schema
                controller.schema.add_table(table)
                
                # Add to UI list
                self.window.ui.tableList.addItem(table_name)
                
                # Draw on canvas
                controller.table_controller.draw_table_on_canvas(table)
                
                # Update SQL display
                controller.table_controller.update_sql()
                
                print(f"✅ Table '{table_name}' added to canvas with {len(columns)} columns")
                
        except Exception as e:
            print(f"❌ Error adding table to canvas: {e}")

    def parse_columns_from_sql(self, sql):
        """Parse column definitions from CREATE TABLE SQL"""
        columns = []
        
        # Find content between parentheses
        start = sql.find('(')
        end = sql.rfind(')')
        if start == -1 or end == -1:
            return columns
        
        content = sql[start+1:end].strip()
        
        # Split by commas, but be careful with nested parentheses
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for line in lines:
            # Remove trailing comma if exists
            if line.endswith(','):
                line = line[:-1].strip()
            
            # Skip constraint lines
            if line.upper().startswith('CONSTRAINT') or line.upper().startswith('PRIMARY KEY') or line.upper().startswith('FOREIGN KEY'):
                continue
            
            # Parse column definition
            parts = line.split()
            if len(parts) >= 2:
                col_name = parts[0].strip()
                col_type = parts[1].strip().upper()
                
                # Check for primary key
                is_pk = 'PRIMARY KEY' in line.upper()
                
                columns.append({
                    'name': col_name,
                    'type': col_type,
                    'primary_key': is_pk
                })
        
        return columns