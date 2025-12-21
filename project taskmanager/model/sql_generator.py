def generate_sql(schema):
    sql = ""
    for table in schema.tables:
        sql += f"CREATE TABLE {table.name} (\n"
        cols = []
        for attr in table.attributes:
            line = f" {attr.name} {attr.data_type}"
            if attr.primary_key:
                line += " PRIMARY KEY"
            cols.append(line)
        sql += ",\n".join(cols)
        sql += "\n);\n\n"
    return sql