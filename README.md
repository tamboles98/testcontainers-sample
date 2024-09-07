# testcontainers-sample

**Author:** tamboles98

This is a dummy fastapi application for me to play with and demostrate the capabilities
of [Testcontainers](https://testcontainers.com/)

## Motivation
In my experience, one of the more challengings parts of developing tests for any application is always how to test its interactions with external resources. In many cases, this interactions involve very complex logic and rich interfaces, like a SQL database and an ORM. Trying to mock this behaviour is usually gargantuan task with very poor results, because:

1. Lack of knowledge of the underlying service: Due to a lack of knowledge or incorrect assumptions, it's very easy to end up with a mock that unprecise, and doesn't correctly reproduce the logic of the real service
2. Mocks are to shallow: Due to the sheer size and openess of a system like an orm, usually any mock will only reproduce those methods that are used by the code being tested. This leads to fragile test that fail at the smallest refactor and that test for implementation, not for functionality.

For this reason, I have found more success running the test over a real instance of a service rather than trying to simulate/mock any behaviour. However, setting up this underlying infrastructure in order to test, can be difficult. Testcontainers offers a generic approach to test interactions with almost any service, and already has built-in extensions that help you test many of the most common dependecies. I wanted to test its capabilities

## The app
> Note: This is a dummy app

This is a simple app that manages reviews for pieces of media, it handles:
* Users: That can create reviews
* MediaType: Books, movies, games, etc
* Media: Pieces of media
* Authors: Authors of pieces of media
* Reviews. Reviews made by authors with their opinion on some piece of media

## Features
* A fastapi application
* Tests that test database interactions against a Postgres database running locally in Docker thanks to Testcontainers. The database is provisioned every time the tests run.
* A GitHub actions pipeline that applies the Ruff linter, runs the tests and checks for the coverage of tests.

## Conclusions
I was very satisfied by the results, Testcontainers ran flawlessly just by having Docker installed on my machine, and I also had no issue making it run inside a GitHub workflow. The only negative point is that the Testcontainers documentation for python is lacking. They give a pretty good example using postgres, but there is very little explanation on how to extrapolate that to other services. Specially, I found very little documentation on plugins for other popular dependencies besides postgres.
