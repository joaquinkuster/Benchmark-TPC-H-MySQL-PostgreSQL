import re, os

SRC = "queries_raw"
DST_PG = "queries_postgres"
DST_MY = "queries_mysql"
os.makedirs(DST_PG, exist_ok=True)
os.makedirs(DST_MY, exist_ok=True)

for i in range(1, 23):
    with open(f"{SRC}/q{i}.sql") as f:
        sql = f.read()

    # Quitar comandos de cliente Sybase/SQL Server
    sql = re.sub(r'\nset rowcount\s+-?\d+\s*\ngo\s*$', '\n', sql, flags=re.IGNORECASE)
    sql = re.sub(r'^-- using.*\n', '', sql)

    # --- Versión PostgreSQL: sacar el "(N)" de precisión del interval ---
    pg = re.sub(r"(interval\s+'\d+'\s+\w+)\s*\(\d+\)", r"\1", sql, flags=re.IGNORECASE)

    # --- Versión MySQL: interval 'N' unit  ->  INTERVAL N unit ---
    my = re.sub(r"interval\s+'(\d+)'\s+(\w+)(?:\s*\(\d+\))?", r"INTERVAL \1 \2", sql, flags=re.IGNORECASE)

    # --- Q13: MySQL/MariaDB no soporta alias de columnas en subconsulta derivada ---
    my = my.replace("count(o_orderkey)\n", "count(o_orderkey) as c_count\n")
    my = re.sub(r"as c_orders\s*\(c_custkey,\s*c_count\)", "as c_orders", my)

    with open(f"{DST_PG}/q{i}.sql", "w") as f:
        f.write(pg)
    with open(f"{DST_MY}/q{i}.sql", "w") as f:
        f.write(my)

print("Listo: 22 consultas adaptadas en queries_postgres/ y queries_mysql/")
