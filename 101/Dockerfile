# Use the official Ubuntu base image
FROM ubuntu:latest

# Install dependencies: Apache2, Cowsay, and Fortune
RUN apt-get update && \
    apt-get install -y apache2 cowsay fortune && \
    apt-get clean

# Generate a fortune, pipe it to cowsay, wrap it in HTML <pre> tags, and save it as an HTML file
RUN echo "<html><body><pre>" > /var/www/html/index.html && \
    /usr/games/fortune | /usr/games/cowsay >> /var/www/html/index.html && \
    echo "</pre></body></html>" >> /var/www/html/index.html

# Configure Apache to serve the HTML file
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Expose port 80 for the web server
EXPOSE 80

# Start Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
