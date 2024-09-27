# Use the official Ubuntu base image
FROM ubuntu:latest

# Install Apache and necessary utilities
RUN apt-get update && \
    apt-get install -y apache2 apache2-suexec-pristine libapache2-mod-fcgid curl cowsay fortune mysql-client && \
    apt-get clean

# Enable CGI module in Apache
RUN a2enmod cgi

# Copy the CGI script to the appropriate directory
COPY get-fortune.cgi /usr/lib/cgi-bin/get-fortune.cgi
RUN chmod +x /usr/lib/cgi-bin/get-fortune.cgi

# Configure Apache to serve CGI scripts
RUN echo "ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/" > /etc/apache2/conf-enabled/cgi-bin.conf && \
    echo "<Directory /usr/lib/cgi-bin>" >> /etc/apache2/conf-enabled/cgi-bin.conf && \
    echo "    Options +ExecCGI" >> /etc/apache2/conf-enabled/cgi-bin.conf && \
    echo "    AddHandler cgi-script .sh" >> /etc/apache2/conf-enabled/cgi-bin.conf && \
    echo "</Directory>" >> /etc/apache2/conf-enabled/cgi-bin.conf

# Expose port 80 for the web server
EXPOSE 80

# Start Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
