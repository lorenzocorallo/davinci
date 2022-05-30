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


def make_msg(content, sender):
    return {"content": content, "sender": sender, "timestamp": get_current_time()} 

@app.route("/", methods=["GET"])
def index():
    if not session.get('logged_in'): return redirect(url_for("login"))
    if not session.get("ai_username"): return redirect(url_for("setup"))
    ai_username = session.get("ai_username")
    
    if session.get("dialog") == None:
        session["dialog"] = []

    return render_template("index.html", ai_username=ai_username)

@app.route("/dialog", methods=["GET"])
def dialog():
    if not session.get('logged_in') or not session.get("ai_username"): return "", 401
    if session.get("dialog") == None: return "", 404
    if len(session.get("dialog")) == 0: return {"dialog": []}, 404
    return {"dialog": session.get("dialog")}, 200

@app.route("/send", methods=["POST"])
def send():
    if not session.get('logged_in') or not session.get("ai_username") or session.get("dialog") == None: return "", 401
    dialog = session.get("dialog")
    ai_username = session.get("ai_username")
    
    content = request.json["question"]
    question = make_msg(content, "Tu")
    dialog.append(question)
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=make_prompt(dialog),
        temperature=0.7,
        max_tokens=400,
        top_p=1,
        stop="\n",
        frequency_penalty=0.2,
        presence_penalty=0.2,
    )
    
    answer = make_msg(response.choices[0].text, ai_username)
    dialog.append(answer)
    session["dialog"] = dialog
    # print(answer, answer.serialize())
    # return {"message": answer.serialize()}, 200
    return {"message": answer}, 200

@app.route("/clear", methods=["POST"])
def clear():
    session["dialog"] = []
    session["ai_username"] = ""
    return redirect(url_for("index"))

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if not session.get('logged_in'): return redirect(url_for("login"))
    if request.method == "POST":
        session["dialog"] = []
        name = request.form["name"]
        session["ai_username"] = name.capitalize()
        
        return redirect(url_for("index", ai_username=session["ai_username"]))

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
    prompt = "Dialogo in lingua italiana.\n"
    ld = dialog.copy()
    if len(ld) > 9:
        ld = ld[len(ld) - 9:]
    for message in ld:
        prompt += f"{message['sender']}: {message['content']}\n"
    prompt += session.get("ai_username") + ":"
    return prompt

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5002)

