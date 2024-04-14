# Iconian Gateway

When running `client`, it communicates with the server to determine whether the Wordle guesses are correct.  `fake_server.py` simulates a fake server which always replies with the win condition.  Start the fake server, start `client` with `127.0.0.1:7503`, and submit any guess.  The client will print the flag.
