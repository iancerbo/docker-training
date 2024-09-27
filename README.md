# Docker Training

## 101

[Presentation](https://cerboehr-my.sharepoint.com/:p:/g/personal/ian_johnson_cer_bo/Ec7OJ3fTUstPpCSws--bNOgBfHKWsDKrzCyVUQDNs07MTA?e=PQuSAo)

First, let's grab a copy of an `ubunutu` image from Docker Hub:

```shell
docker pull ubuntu
```

Now that we have this, we can run a container of the image. This runs a process inside of an environment.

```shell
docker run ubuntu ls
docker run ubuntu echo "Hello world"
docker run ubuntu bash
```

Why doesn't this work? Let's check the processes.

```shell
docker ps -a
```

This is happening because bash exited. If we want an interactive shell, we need to tell docker to give us a tty.

```shell
docker run -it ubuntu bash
```

We're in! Now what? Let's install some packages and run a command.

```shell
apt-get update
apt-get install -y cowsay fortune
chmod +x /usr/games/cowsay
/usr/games/fortune | /usr/games/cowsay
exit
```

Nice! We got output as expected. Okay, let's run it again.

```shell
docker run -it ubuntu bash
/usr/games/fortune | /usr/games/cowsay
exit
```

Huh? It isn't there. Why not? Because containers do NOT save state. Containers are intended to run only. If we want state, we need to use an update image.

To solve this, we'll create a Dockerfile.

```shell
touch Dockerfile
$EDITOR Dockerfile
```

```Dockerfile
# Use the official Ubuntu base image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y cowsay fortune && \
    apt-get clean

# Set cowsay to be executable by default
RUN chmod +x /usr/games/cowsay

# Run fortune and pipe it to cowsay
CMD /usr/games/fortune | /usr/games/cowsay
```

And then build a docker image from it.

```shell
docker build -t moodini .
docker run moodini
```

And it works! Great!

Now we have a simple process running in a container. Let's wrap this up behind a web server. Update the Dockerfile.

```Dockerfile
# Use the official Ubuntu base image
FROM ubuntu:latest

# Install dependencies: Apache2, Cowsay, and Fortune
RUN apt-get update && \
    apt-get install -y apache2 cowsay fortune && \
    apt-get clean

# Generate a fortune and pipe it to cowsay, then save the output as an HTML file
RUN /usr/games/fortune | /usr/games/cowsay > /var/www/html/index.html

# Configure Apache to serve the HTML file
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Expose port 80 for the web server
EXPOSE 80

# Start Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]
```

And then we build a new image. We add a flag to run the container in daemon mode (background) and to map the port.

```shell
docker build -t moodini-web .
docker run moodini-web
docker run -d -p 8080:80 moodini-web
```

Great, now let's visit the page at http://locahost:8080/

This works, but it gives us an ugly response. Let's make it prettier! Update the Dockerfile again.

```Dockerfile
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
```

Before we build again, let's talk about how Docker images are versioned: tags. We'll add a `v2` tag for this image to demonstrate.

```shell
docker build -t moodini-web:v2 .
docker run -d -p 8080:80 moodini-web:v2
```

Uh oh! Why didn't this work? Because we never stopped the last container, which means it's still running (and listening on port 8080). So we have run into a port collision. Let's stop the other container.

```shell
docker ps
docker ps -q
docker stop $(docker ps -q)
docker run -d -p 8080:80 moodini-web:v2
```

Let's visit the page again at http://locahost:8080/

And now our `moodini-web` service outputs something a little prettier.

Great! What's next?

- Adding a database
- Using docker compose
- Understanding the docker setup for our apps

## 102

[Presentation](https://cerboehr-my.sharepoint.com/:p:/g/personal/ian_johnson_cer_bo/ERU8tAMNrTpEjy6MwjgUpY0B1QjNJJrjKIUSf7-LJtH3yQ?e=M3UZkq)

For containers to be able to talk to each other, they must be on the same network. Just like with hardware, two machines must be on the same network to talk to each other. Docker networks are _essentially_ virtual networks.

First, let's create a network.

```shell
docker network create my-network
```

Now, we can run two containers on this network.

```shell
docker run -d \
  --name my-db-container \
  --network my-network \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  mysql:latest

docker run -d \
  --name my-app-container \
  --network my-network \
  -e DB_HOST=my-db-container \
  -e DB_PASSWORD=rootpassword \
  my-app-image:latest
```

This is great! We have two containers running in the background that are on the same network. One container has the database, and the other has the application. This kind of service segregation is great for scaling purposes. However, our data is _still_ temporary. To get it to persist, we need to add a volume.

Docker volumes are a way to persist data used by containers. To add the volume, we can pass a `-v` flag.

```shell
docker run -d \
  --name my-db-container \
  --network my-network \
  -v db-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  mysql:latest

docker run -d \
  --name my-app-container \
  --network my-network \
  -v app-data:/usr/src/app \
  -e DB_HOST=my-db-container \
  -e DB_PASSWORD=rootpassword \
  my-app-image:latest
```

Awesome! Now we have two containers on the same network that _also_ persist data.

You may be wondering about the details of this network. To find those details, we can run the following command.

```shell
docker network inspect my-network
```

This gives us lots of details in case we need to debug, including what containers are attached to the network.

In addition to syncing data to the filesystem, we can wrap this up in a real docker volume, which gives it a name _and_ makes it more predictable.

```shell
docker volume create shared-data
```

Here's what our commands look like using the named volume, instead of the local filesystem.

```shell
docker run -d \
  --name my-db-container \
  --network my-network \
  -v shared-data:/shared \
  mysql:latest

docker run -d \
  --name my-app-container \
  --network my-network \
  -v shared-data:/shared \
  my-app-image:latest
```

This is all great, but it is **NOT** _the way_. One of the greatest benefits of Docker is not having to manage infrastructure, so let's stop using docker to manage infrastructure manually. How do we do that? Well, _all_ of these details can be defined in a `docker-compose.yml` file. With this file in place, we can use the `docker-compose` command to gain the same benefits without running a ton of commands.

Returning to our example, here's how that looks for our `moodini-web` service, now backed by a real database!

First, we need a Dockerfile.

```dockerfile
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
```

Notice that our Dockerfile references a cgi script. This is what that script looks like.

```shell
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
```

Finally, we create a `docker-compose.yml` file. This file defines declaratively what the service looks like.

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:80"
    depends_on:
      - db
    environment:
      MYSQL_HOST: db
      MYSQL_USER: root
      MYSQL_PASSWORD: password
      MYSQL_DATABASE: fortunes

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: fortunes
    volumes:
      - db-data:/var/lib/mysql
      - ./db:/docker-entrypoint-initdb.d
    ports:
      - "3306:3306"
    platform: linux/x86_64

volumes:
  db-data:
```

Fantastic! Now that we have all of this defined in files, we can start the entire service using just one command.

```shell
docker-compose up
```

Let's visit the newly defined service at http://locahost:8080/cgi-bin/get-fortune.cgi

Now, we can referesh the page and we get _dynamic_ results! Huzzah!

You may be wondering how the database has data in it to begin with, for the cgi script to be able to query. This is actually defined in the `db` folder. It's mounted to `docker-entrypoint-initdb.d` inside the container. As a result, the database is populated with everthing in the `db/init.sql` file.

```sql
CREATE TABLE fortunes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL
);

INSERT INTO fortunes (message) VALUES ('You will have a great day!');
INSERT INTO fortunes (message) VALUES ('Something wonderful is about to happen.');
INSERT INTO fortunes (message) VALUES ('Be prepared for a pleasant surprise.');
```

And that's it. All of the commands and data have been defined inside files, which can then be version controlled. This means we can manage our infrastructure using code!

Now that we have seen what this looks like with a toy example, and we have a basic understanding of docker images, containers, networks, and volumes, we have the tools and knowledge to delve into how we use Docker for the [MDHQ](https://github.com/MD-HQ/MDHQ2.4) and [Frodo](https://github.com/MD-HQ/frodo) projects.
