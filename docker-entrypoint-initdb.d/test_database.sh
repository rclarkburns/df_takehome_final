#!/usr/bin/env bash
echo "Creating test database (${TEST_DB_NAME}...)"
mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${TEST_DB_NAME}; GRANT ALL PRIVILEGES ON ${TEST_DB_NAME}.* TO '${MYSQL_USER}'@'%'; FLUSH PRIVILEGES;"
