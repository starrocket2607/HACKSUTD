from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello():
  if request.method == "POST":
    hrs = request.form["hrs"]
  
  return render_template("index.html")

