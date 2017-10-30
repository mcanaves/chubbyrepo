# Chubbyrepo

Project to play with Python 3, Docker and apply [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html) principles with python


## Quickstart

### Prerequisites
You’ll need at least Docker 1.17.

If you don’t already have it installed, follow the instructions for your OS:
* On Mac OS X, you’ll need [Docker for Mac](https://docs.docker.com/docker-for-mac/)
* On Windows, you’ll need [Docker for Windows](https://docs.docker.com/docker-for-windows/)
* On Linux, you’ll need [docker-engine](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/#install-compose)

### Configure
This project relies extensively on Github API and is mandatory to set a [personal github token](https://github.com/blog/1509-personal-api-tokens) as an environment variable `GITHUB_API_KEY`. 
```bash
$ export GITHUB_API_KEY={YOUR_API_TOKEN}
```

### Build and boot the system
This can take a while, especially the first time you run this particular command on your development system:
```bash
$ docker-compose up --build
```
but in the subsequent runs you won't need to build the system and boot will occur quickly: 
```bash
$ docker-compose up 
```

## Endpoints
The following endpoints are currently supported:

| Endpoint                                  | Description |
| ----------------------------------------- | ----------- |
| `/organizations/{org_name}/stats`         | Returns the number of repositories and the biggest repository of the given organization. |
| `/chubbiest_repositories[?limit={n}]`     | Returns the n-th biggest repositories. By default n is 10. |

## Development
To work on the Chubbyrepo codebase, you'll want to clone the repository, 
and create a Python virtualenv with the project requirements installed:
```bash
$ git clone git@github.com:mcanaves/chubbyrepo.git
$ cd chubbyrepo
$ ./scripts/setup
```
To run the tests and code linting:
```bash
$ ./scripts/test
$ ./scripts/lint
```

## Changelog

### 0.1 Release
* Initial release

<p align="center"><i>Chubbyrepo is <a href="https://github.com/mcanaves/chubbyrepo/blob/master/LICENSE">BSD licensed</a> code.<br/>Designed & built in Pollença City.</i><br/>&mdash; :sunglasses: &mdash;</p>

