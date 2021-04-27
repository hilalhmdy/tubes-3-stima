from flask import Flask,redirect,render_template,request,url_for
from backend import *

app = Flask(__name__)

# halaman utama
@app.route('/', methods=["POST","GET"])
def main():

    # render main.html
    return render_template("main.html")

# jalanin program
if __name__ == "__main__":
    app.run(debug=True)