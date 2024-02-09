# Wordle

Mock of the game Wordle in Python Using FastApi with REST.

## How to run game
First install
<ul>
    <li>pip install pydantic</li>
    <li>pip install fastapi</li>
    <li>pip install uvicorn</li>
    <li>pip install cachetools</li>
    <li>pip install pytest</li>
    <li>pip install pytest-cov</li>
    <li>pip install httpx</li>
    <li>pip install importlib-metadata</li>
</ul>
To run you can:<br>
Run: python main.py<br>
or<br>
Run: uvicorn main:app --reload

### How to run game tests:
Run: pytest

### How to run game code coverage:
Run: pytest --cov

## How to run solver:
Run cargo run

## How to play
<ul>
    <li>
        Run this CURL:
        <br>curl --location 'http://127.0.0.1:8000/start'<br>
        it will return something like: { "session": "450d1952-9052-4bc6-b05b-7940158edc9d" } <br>
        copy the session key
    </li>
    <br>
    <li>
        Run this CURL with the key instead of {session} and replace the {word} with the word you want to use:
        <br>curl --location --request POST 'http://127.0.0.1:8000/play/session/{session}' \
--header 'Content-Type: text/plain' \
--data '{word}'
    </li>
</ul>

## TODO
<ol>
    <li>Python, think how to solve issue with 100% coverage without exposing picked word</li>
    <li>Add more edge cases implementations to solver</li>
    <li>Tests for solver</li>
    <li>Docker</li>
    <li>Oauth with Google and Postgres to have scoreboard + endpoint to get user specific scores</li>
</ol>

## Author
Github: [barakadax](https://github.com/barakadax)
