import duckdb

# 1. Connect to (or create) the DuckDB database
con = duckdb.connect("condo_sql.duckdb")

# 2. Load and run the .sql file
with open("dads5001db.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()
    con.execute(sql_script)

#/workspaces/DADS5001-Condo/dads5001db.sql

# 3. Check what tables were created
tables_df = con.execute("SHOW TABLES").df()
print("Tables in condo.duckdb:")
print(tables_df)

# 4. (Optional) Describe a table
schema_df = con.execute("PRAGMA table_info('condo')").df()
print("Schema of 'condo' table:")
print(schema_df)

con.close()