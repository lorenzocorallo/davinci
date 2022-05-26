# DaVinci

A Flask app to use [OpenAI](https://openai.com/api/) api as a chatbot.
The project is built on Python for backend and logic, on HTML5 and CSS for the frontend.
Since the Api has [price/call](https://openai.com/api/), it's required that the user uses his own key.

## Requirements

- Python 3
- Virtual environment for Python3  
  Linux/Mac:
  ```
  python3 -m pip install virtualenv
  ```
  Windows:
  ```
  python -m pip install virtualenv
  ```

## Installation

To start using this project, you need to follow these steps:

1. Download source code from [here](https://github.com/lorenzocorallo/davinci/archive/refs/heads/master.zip) or from the _green button above file tree_
2. Create the virtual environment
   ```
   python -m venv venv
   ```
3. Enter into virtual environment<br>
   Linux
   ```
   source venv/bin/activate
   ```
   Windows
   ```
   . venv/Scripts/activate
   ```
4. Install requirements:
   ```
   pip install -r requirements.txt
   ```

## Quick start

The first time you need to set up env variables.  
Rename `.env.example` to `.env` and set:

- OPENAI_API_KEY -> secret api key from OpenAI
- PASSWORD -> the login password for Flask UI

To start as development server:

1. Enable virtual environment, if not already in (as Installation #3)
2. Run
   ```
   flask run
   ```

## Deployment

To deploy the app you can use a package manager as PM2, these are the step with it:

1. Enable virtual environment, if not already in (as Installation #3)
2. Run
   ```
   pm2 run --name "put a name of your choice here" app.py --interpreter python3
   pm2 save
   ```
3. The app will be available on `127.0.0.1:5002` or `localhost:5002` _(you can change port in `app.py` in `serve` command)_

## Code strucutre

This web app is made on Flask.<br>
You can modify HTML files in `templates/` folder and CSS in `static/`; <br> you can also add other static files (such as JS and images) in `static/` and then link in HTML as `{{ url_for('static', filename='*****.***') }}`. <br>
All the logic is in `app.py`, including Flask routes.

## Credits

This project is made by Lorenzo Corallo (developer) and Luis Dodaj (creator, developer) for a school assignment.
