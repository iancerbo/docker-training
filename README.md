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
nvim Dockerfile
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

Next time!
