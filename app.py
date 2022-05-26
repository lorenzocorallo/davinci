import os
import time
import openai
from flask import Flask, redirect, render_template, request, url_for, session

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(12)
openai.api_key = os.getenv("OPENAI_API_KEY")
PASSWORD = os.getenv("PASSWORD")

def get_current_time():
    return time.strftime("%H:%M")

class Message:
    def __init__(self, content, sender):
        self.content = content
        self.sender = sender
        self.timestamp = get_current_time()

dialog = []
ai_username = ""

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get('logged_in'): return redirect(url_for("login"))
    if ai_username == "": return redirect(url_for("setup", dialog=dialog))
    
    if len(dialog) == 0:
        dialog.append(Message(f"Ciao, sei in contatto con {ai_username}, invia il primo messaggio.", "DaVinci"))
    
    if request.method == "POST":
        content = request.form["question"]
        question = Message(content, "Tu")
        dialog.append(question)
        print(make_prompt(dialog))
        
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=make_prompt(dialog),
            temperature=0.7,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
        )
        
        answer = Message(response.choices[0].text.strip('\n'), ai_username)
        dialog.append(answer)
        return redirect(url_for("index"))

    return render_template("index.html", dialog=dialog, ai_username=ai_username)


@app.route("/clear", methods=["POST"])
def clear():
    global dialog
    global ai_username
    dialog = []
    ai_username = ""
    return redirect(url_for("index"))

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if not session.get('logged_in'): return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        global ai_username
        ai_username = name
        
        return redirect(url_for("index"))

    return render_template("setup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == PASSWORD:
            session['logged_in'] = True
        
            return redirect(url_for("index"))
        return redirect(url_for("login", wrong=True))
        
    return render_template("login.html", wrong=request.args.get("wrong"))

@app.route("/logout", methods=["POST"])
def logout():
    session['logged_in'] = False
    return redirect(url_for("login"))
        

def make_prompt(dialog):
    prompt = "Lingua italiana\n"
    ld = dialog[1:]
    if len(ld) > 4:
        ld = ld[len(ld) - 4:]
    for message in ld:
        prompt += f"{message.sender}: {message.content}\n"
    prompt += ai_username + ":"
    return prompt

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5002)

