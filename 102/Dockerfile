# Use the official Ubuntu base image
FROM ubuntu:latest

# Install dependencies: Apache2, Cowsay, Fortune, MySQL client
RUN apt-get update && \
    apt-get install -y apache2 cowsay fortune mysql-client && \
    apt-get clean

# Enable CGI module in Apache
RUN a2enmod cgi

# Copy the CGI script to the appropriate directory
COPY get-fortune.cgi /usr/lib/cgi-bin/get-fortune.cgi
RUN chmod +x /usr/lib/cgi-bin/get-fortune.cgi

# Configure Apache to allow CGI execution
RUN echo "<Directory /usr/lib/cgi-bin>" > /etc/apache2/sites-available/000-default.conf && \
    echo "    Options +ExecCGI" >> /etc/apache2/sites-available/000-default.conf && \
    echo "    AddHandler cgi-script .cgi" >> /etc/apache2/sites-available/000-default.conf && \
    echo "</Directory>" >> /etc/apache2/sites-available/000-default.conf

# Expose port 80 for the web server
EXPOSE 80

# Start Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
