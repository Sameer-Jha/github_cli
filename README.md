# A cli based tools for basic github platform operation like creating a new repo, branch etc.
## Now no need to leave command line for basic github tasks.

## Installation

### Steps to be taken before Installtaion
*** Set these environment variable***
>  1. set **GITAUTH_TOKEN** as github auth token. [visit this for help](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) with auth token generation
>  2. set **GH_UNAME** as Github user name 

### Installtion process 
***(if you have access using root isn't necessary)***
```
$ sudo pip install -r requirements.txt

$ sudo python setup.py install
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run github cli application

$ github --help


### run pytest / coverage

$ make test
```


## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `github`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it github --help
```
