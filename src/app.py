from flask import Flask, render_template, request
from os import path
from backend import balasan

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/get")
def get_bot_response():

    userText = request.args.get('msg')

    return balasan(userText)

if __name__ == "__main__":
    app.run(debug = True)