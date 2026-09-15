#!/bin/bash
PSQL='/mnt/c/Program Files/PostgreSQL/16/bin/psql.exe'
MYSQL='/mnt/c/xampp/mysql/bin/mysql.exe'

echo "=== PostgreSQL ==="
for i in $(seq 1 22); do
  err=$("$PSQL" -U postgres -d tpch -f "queries_postgres/q$i.sql" 2>&1 >/dev/null)
  if [ -z "$err" ]; then
    echo "Q$i: OK"
  else
    echo "Q$i: ERROR -> $(echo "$err" | head -1)"
  fi
done

echo ""
echo "=== MySQL/MariaDB ==="
for i in $(seq 1 22); do
  err=$("$MYSQL" -u root tpch < "queries_mysql/q$i.sql" 2>&1 >/dev/null)
  if [ -z "$err" ]; then
    echo "Q$i: OK"
  else
    echo "Q$i: ERROR -> $(echo "$err" | head -1)"
  fi
done
