from model.table_model import Table, Attribute
from model.relationship_model import Relationship
from PySide6.QtWidgets import (
    QInputDialog, QMessageBox, QGraphicsRectItem, QGraphicsTextItem, 
    QGraphicsLineItem
)
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtCore import Qt
import traceback

class TableController:
    def __init__(self, schema, window):
        self.schema = schema
        self.window = window

        # Initialize canvas
        if hasattr(self.window.ui, 'schemaCanvas') and self.window.ui.schemaCanvas:
            if hasattr(self.window.ui.schemaCanvas, 'scene'):
                self.window.ui.schemaCanvas.scene().clear()

        self.window.ui.addTableButton.clicked.connect(self.create_table)
        self.window.ui.deleteTableButton.clicked.connect(self.delete_table)
        self.window.ui.editAttributeButton.clicked.connect(self.edit_attribute)
        self.window.ui.deleteAttributeButton.clicked.connect(self.delete_attribute)
        self.window.ui.addRelationshipButton.clicked.connect(self.add_relationship_dialog)
        self.window.ui.deleteRelationshipButton.clicked.connect(self.delete_relationship)

        # Variables for table positions
        self.table_positions = {}
        self.next_x = 20
        self.next_y = 20

    # ---------------- TABLE ----------------

    def create_table(self):
        name = self.window.ui.tableNameInput.text().strip()
        if not name:
            QMessageBox.warning(self.window, "Warning", "Please enter table name")
            return

        if any(t.name == name for t in self.schema.tables):
            QMessageBox.warning(self.window, "Error", "Table already exists")
            return

        table = Table(name)
        self.schema.add_table(table)
        self.window.ui.tableList.addItem(name)
        self.window.ui.tableNameInput.clear()

        # Add columns
        self.add_attributes_dialog(table)
        
        # Draw table on Canvas
        self.draw_table_on_canvas(table)
        
        # Update SQL
        self.update_sql()
        
        # Load schema to database
        self.load_schema_to_db()

    def draw_table_on_canvas(self, table):
        """Draw table on Canvas"""
        attributes_list = []
        for attr in table.attributes:
            attributes_list.append({
                'name': attr.name,
                'type': attr.data_type,
                'pk': attr.primary_key
            })
        
        # Calculate height
        height = 40 + len(attributes_list) * 25
        
        # Draw main rectangle
        rect = QGraphicsRectItem(self.next_x, self.next_y, 200, height)
        rect.setBrush(QBrush(QColor(0, 0, 139)))  # أزرق غامق (Dark Blue)

        rect.setPen(QPen(Qt.black, 2))
        self.window.ui.schemaCanvas.scene().addItem(rect)
        
        # Draw table title
        title = QGraphicsTextItem(table.name)
        title.setDefaultTextColor(Qt.blue)
        title.setPos(self.next_x + 10, self.next_y + 10)
        self.window.ui.schemaCanvas.scene().addItem(title)
        
        # Draw line under title
        line = QGraphicsLineItem(self.next_x + 5, self.next_y + 35, 
                                self.next_x + 195, self.next_y + 35)
        line.setPen(QPen(Qt.gray, 1))
        self.window.ui.schemaCanvas.scene().addItem(line)
        
        # Draw columns
        for i, attr in enumerate(attributes_list):
            attr_text = f"• {attr['name']} : {attr['type']}"
            if attr.get('pk', False):
                attr_text += " (PK)"
                
            text_item = QGraphicsTextItem(attr_text)
            text_item.setPos(self.next_x + 10, self.next_y + 45 + i * 25)
            self.window.ui.schemaCanvas.scene().addItem(text_item)
        
        # Save table position
        self.table_positions[table.name] = {
            'x': self.next_x,
            'y': self.next_y,
            'rect': rect
        }
        
        # Update positions for next table
        self.next_x += 220
        if self.next_x > 600:
            self.next_x = 20
            self.next_y += 200

    def delete_table(self):
        item = self.window.ui.tableList.currentItem()
        if not item:
            QMessageBox.warning(self.window, "Warning", "Please select a table to delete")
            return

        name = item.text()
        
        # Confirm deletion
        reply = QMessageBox.question(
            self.window, "Confirm Delete",
            f"Are you sure you want to delete table '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return

        # Find and remove the table
        table_to_delete = None
        for table in self.schema.tables:
            if table.name == name:
                table_to_delete = table
                break
        
        if table_to_delete:
            self.schema.tables.remove(table_to_delete)
            self.window.ui.tableList.takeItem(self.window.ui.tableList.row(item))
            
            # Remove from Canvas
            if name in self.table_positions:
                del self.table_positions[name]
            
            # Redraw canvas
            self.redraw_canvas()
            
            # Update SQL
            self.update_sql()
            
            QMessageBox.information(self.window, "Success", f"Table '{name}' deleted successfully")

    # ---------------- ATTRIBUTES ----------------

    def add_attributes_dialog(self, table):
        while True:
            attr_name, ok = QInputDialog.getText(
                self.window, "Add Attribute", "Attribute name:"
            )
            if not ok or not attr_name:
                break

            data_type, ok = QInputDialog.getItem(
                self.window, "Data Type", "Select data type:",
                ["INTEGER", "TEXT", "VARCHAR(255)", "REAL", "BOOLEAN", "DATE", "DATETIME"], 
                0, False
            )
            if not ok:
                break

            pk, ok = QInputDialog.getItem(
                self.window, "Primary Key", "Is Primary Key?",
                ["No", "Yes"], 0, False
            )
            if not ok:
                break

            # Add the column
            table.add_attribute(Attribute(attr_name, data_type, pk == "Yes"))
            
            # Ask if user wants to add another column
            again, ok = QInputDialog.getItem(
                self.window, "Continue", "Add another attribute?",
                ["Yes", "No"], 0, False
            )
            if not ok or again == "No":
                break

    def edit_attribute(self):
        table = self.get_selected_table()
        if not table:
            QMessageBox.warning(self.window, "Warning", "Please select a table first")
            return
            
        if not table.attributes:
            QMessageBox.warning(self.window, "Warning", "This table has no attributes")
            return

        names = [a.name for a in table.attributes]
        attr_name, ok = QInputDialog.getItem(
            self.window, "Edit Attribute", "Select attribute to edit:", names, 0, False
        )
        if not ok:
            return

        # Find the attribute
        attr = None
        for a in table.attributes:
            if a.name == attr_name:
                attr = a
                break
                
        if not attr:
            return

        # Edit name
        new_name, ok = QInputDialog.getText(
            self.window, "Edit Attribute Name", 
            "New attribute name:", text=attr.name
        )
        if ok and new_name:
            attr.name = new_name

        # Edit data type
        data_type, ok = QInputDialog.getItem(
            self.window, "Edit Data Type", "Select new data type:",
            ["INTEGER", "TEXT", "VARCHAR(255)", "REAL", "BOOLEAN", "DATE", "DATETIME"],
            0, False
        )
        if ok:
            attr.data_type = data_type

        # Edit Primary Key
        pk, ok = QInputDialog.getItem(
            self.window, "Edit Primary Key", "Primary Key?",
            ["No", "Yes"], 0, False
        )
        if ok:
            attr.primary_key = (pk == "Yes")

        # Redraw canvas and update SQL
        self.redraw_canvas()
        self.update_sql()

    def delete_attribute(self):
        table = self.get_selected_table()
        if not table:
            QMessageBox.warning(self.window, "Warning", "Please select a table first")
            return
            
        if not table.attributes:
            QMessageBox.warning(self.window, "Warning", "This table has no attributes")
            return

        names = [a.name for a in table.attributes]
        attr_name, ok = QInputDialog.getItem(
            self.window, "Delete Attribute", "Select attribute to delete:", names, 0, False
        )
        if not ok:
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self.window, "Confirm Delete",
            f"Are you sure you want to delete attribute '{attr_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return

        # Remove the attribute
        table.attributes = [a for a in table.attributes if a.name != attr_name]
        
        # Redraw canvas and update SQL
        self.redraw_canvas()
        self.update_sql()
        
        QMessageBox.information(self.window, "Success", f"Attribute '{attr_name}' deleted")

    # ---------------- RELATIONSHIP ----------------

    def add_relationship_dialog(self):
        if len(self.schema.tables) < 2:
            QMessageBox.warning(self.window, "Warning", "Need at least 2 tables to create relationship")
            return

        names = [t.name for t in self.schema.tables]
        t1, ok = QInputDialog.getItem(
            self.window, "Create Relationship", "Select first table:", names, 0, False
        )
        if not ok:
            return
            
        t2, ok = QInputDialog.getItem(
            self.window, "Create Relationship", "Select second table:", names, 0, False
        )
        if not ok or t1 == t2:
            return

        rel_type, ok = QInputDialog.getItem(
            self.window, "Relationship Type", "Select relationship type:",
            ["1-N (One to Many)", "N-N (Many to Many)"], 0, False
        )
        if not ok:
            return

        # Convert to short notation
        rel_type_short = "1-N" if "1-N" in rel_type else "N-N"

        table1 = next(t for t in self.schema.tables if t.name == t1)
        table2 = next(t for t in self.schema.tables if t.name == t2)

        # Create relationship
        relationship = Relationship(table1, table2, rel_type_short)
        self.schema.add_relationship(relationship)
        
        # Draw relationship on Canvas
        self.draw_relationship_on_canvas(relationship)
        
        # Update SQL
        self.update_sql()
        
        QMessageBox.information(
            self.window, "Success", 
            f"Relationship created: {t1} ({rel_type_short}) {t2}"
        )

    def draw_relationship_on_canvas(self, relationship):
        """Draw relationship on Canvas"""
        t1_name = relationship.table1.name
        t2_name = relationship.table2.name
        
        if t1_name in self.table_positions and t2_name in self.table_positions:
            pos1 = self.table_positions[t1_name]
            pos2 = self.table_positions[t2_name]
            
            # Calculate start and end points (from table centers)
            x1 = pos1['x'] + 100  # center of table 1
            y1 = pos1['y'] + 50
            x2 = pos2['x'] + 100  # center of table 2
            y2 = pos2['y'] + 50
            
            # Draw line
            line = QGraphicsLineItem(x1, y1, x2, y2)
            
            if relationship.rel_type == "N-N":
                line.setPen(QPen(QColor(255, 0, 0), 2, Qt.DashLine))
            else:
                line.setPen(QPen(QColor(0, 100, 0), 2))
                
            self.window.ui.schemaCanvas.scene().addItem(line)
            
            # Add relationship type text
            text = QGraphicsTextItem(relationship.rel_type)
            text.setPos((x1 + x2) / 2, (y1 + y2) / 2)
            text.setDefaultTextColor(Qt.darkBlue)
            self.window.ui.schemaCanvas.scene().addItem(text)

    def delete_relationship(self):
        if not self.schema.relationships:
            QMessageBox.warning(self.window, "Warning", "No relationships to delete")
            return

        names = [f"{r.table1.name} ← {r.rel_type} → {r.table2.name}" 
                for r in self.schema.relationships]
        
        choice, ok = QInputDialog.getItem(
            self.window, "Delete Relationship", "Select relationship to delete:", 
            names, 0, False
        )
        if not ok:
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self.window, "Confirm Delete",
            f"Delete this relationship?\n{choice}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return

        # Find and remove the relationship
        index = names.index(choice)
        deleted_rel = self.schema.relationships.pop(index)
        
        # Redraw canvas
        self.redraw_canvas()
        
        # Update SQL
        self.update_sql()
        
        QMessageBox.information(self.window, "Success", "Relationship deleted")

    # ---------------- DRAW ----------------

    def redraw_canvas(self):
        """Redraw everything on Canvas"""
        # Clear canvas
        if hasattr(self.window.ui, 'schemaCanvas') and self.window.ui.schemaCanvas:
            if hasattr(self.window.ui.schemaCanvas, 'scene'):
                self.window.ui.schemaCanvas.scene().clear()
        
        self.table_positions = {}
        
        # Reset positions
        self.next_x = 20
        self.next_y = 20
        
        # Draw all tables
        for table in self.schema.tables:
            self.draw_table_on_canvas(table)
        
        # Draw all relationships
        for rel in self.schema.relationships:
            self.draw_relationship_on_canvas(rel)

    # ---------------- SQL ----------------

    def update_sql(self):
        """Update SQL window"""
        sql = "-- Generated SQL Code\n\n"
        
        # Add table creation code
        for table in self.schema.tables:
            sql += table.generate_create_sql() + "\n\n"
        
        # Add relationship comments
        if self.schema.relationships:
            sql += "-- RELATIONSHIPS --\n"
            for rel in self.schema.relationships:
                sql += f"-- {rel.table1.name} ({rel.rel_type}) {rel.table2.name}\n"
        
        self.window.ui.sqlOutput.setPlainText(sql)
        
        # Load schema to database
        self.load_schema_to_db()

    def load_schema_to_db(self):
        """Load schema to SQLite database"""
        try:
            sql_code = self.window.ui.sqlOutput.toPlainText()
            if sql_code and hasattr(self.window, 'controller'):
                # Pass SQL to SQLController to load it
                self.window.controller.sql_controller.load_schema(sql_code)
        except Exception as e:
            print(f"Error loading schema to DB: {e}")

    def get_selected_table(self):
        """Get the selected table from the list"""
        item = self.window.ui.tableList.currentItem()
        if not item:
            return None
        
        table_name = item.text()
        for table in self.schema.tables:
            if table.name == table_name:
                return table
        return None