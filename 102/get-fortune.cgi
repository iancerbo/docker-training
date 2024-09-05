#!/bin/bash

# Set content-type header
echo "Content-type: text/html"
echo ""

# Connect to the MySQL database and fetch a fortune
MYSQL_HOST="db"
MYSQL_USER="root"
MYSQL_PASSWORD="password"
MYSQL_DATABASE="fortunes"

# Fetch a random fortune from the database
FORTUNE=$(mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -D $MYSQL_DATABASE -e "SELECT message FROM fortunes ORDER BY RAND() LIMIT 1;" -s -N)

# Output the fortune wrapped in cowsay
echo "<html><body><pre>"
echo "$FORTUNE" | /usr/games/cowsay
echo "</pre></body></html>"
