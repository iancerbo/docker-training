# Docker Training

## 101

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

Huh? It isn't there. Why not?

https://github.com/iancerbo/docker-training/blob/61cb2120dd6ac1e4973545486cf52f02f343f366/101/Dockerfile
