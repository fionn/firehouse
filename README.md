# Firehouse

## Deployment

Make a virtual environment with `make venv` and enter it with `source venv/bin/activate`.

Twitter credentials should be stored in the environment variables
`CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET`

To map filmmakers with Twitter handles, include `handles.py`.
This should contain `HANDLE_MAP`, a dictionary of names as keys and Twitter handles as values.

Data from the API should be saved in `data/ffc.json`. It's a static file because updates to the source are unreliable.

Edit the unit files to set the correct paths and copy them to their system locations, then enable the timer.
