# Building the image with the compiled microservices

Move to the root of the socialNetwork app and run
```
sudo docker build -t dsb_build .
```

The image will contain the compiled microservices, for now just UniqueId,
User and SocialGraph (from socialNetwork application).

Now, also in the root run ``./bring_build.sh`` to copy the build directory
from the image, with all the compiled microservices, including also the LLVM
bitcode bundle for each of them as well as the binary.

# Overview of the original execution environment

By looking at the docker-compose.yml file in the root of the socialNetwork app
we see that the microservices have the ./config and ./keys directory binded from
the repo to their fs and have a ``service_completed_successfully`` dependency
on ``config`` container. This container will just run a script which reads an environment
variable that says whether TLS is enabled or not, and rewrites all the
config files in the config directory so as to reflect this condition.

When the microservices containers run, they will read the appropriate config
files.

All the microservices containers will be on the same docker private network
and will see each other's open ports. Moreover, they can resolve each other's
hostname (the hostname of a microservice is the same as its name in the docker-compose.yml file).

However, this hostname, used to perform RPCs, is obtained by the microservice's code
reading a config file.

# Running UserService and SocialGraphService from socialNetwork in isolation

To run only those two microservices, and to do it inside the host and not in
a container, we created a minimal execution environment in this folder.
We brought the whole config/ folder with all the config files here.
Note that the mongodb instance still run inside a docker container.

First, run ``python3 config.py``.
This will rewrite the config files appropiately to disable SSL, disable
jaeger tracing, change the listening port of each microservice to a different
on in order to avoid conflicts, and change the hostname of each microservice to
``localhost``. The last two steps are necessary because previously, each
container had a different hostname and ip address, whereas now they all run
in the host, so they need to point to localhost for resolving and to listen
on different ports.

:wq


## Running the microservices in the host
When running :qq

