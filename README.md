# nepeatbutt

[![Build Status](https://travis-ci.org/nepeat/why_would_you_even.svg?branch=master)](https://travis-ci.org/nepeat/why_would_you_even)

What started out as a joke project turned into a serious bot. Write a better README later.

## Features
* Twitter/Reddit watching (soon)
* Horrible code
* Garbage

## Development / Testing
* Setup your .env file with real information
* `docker-compose build && docker-compose up --abort-on-container-exit`

This is almost the same command that the bot uses to run in production. The only differences is rebuilding every time the command is run and aborting everything if any of the backends containers exit.
