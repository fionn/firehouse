# Firehouse

## Deployment

Make a virtual environment with `make venv` and enter it with `source venv/bin/activate`.

Twitter credentials should be stored in the environment variables
`CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET`.
For systemd, these should be in the `.env` file in the root of this repository, without any `export` directives.

To map filmmakers with Twitter handles, `src/handles.py` is required.
This should contain `HANDLE_MAP`, a dictionary of names as keys and Twitter handles as values.

Data from the API should be saved in `data/films.json`. It can be retrieved with `data/get_films.sh`.

Edit the unit files to set the correct paths and copy them to their system locations, then enable the timer.
