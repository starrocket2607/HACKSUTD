from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
##link to main page
def link():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
