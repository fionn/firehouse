# Firehouse

## Deployment

Make a virtual environment with `make venv` and enter it with `source venv/bin/activate`.

Twitter credentials should be stored in the environment variables
`CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET`.
For systemd, these should be in the `.env` file in the root of this repository, without any `export` directives.

Data from the API should be saved in `data/films.json`. It can be retrieved with `data/get_films.sh`.

Link the unit files to their system locations, then enable the timer.
