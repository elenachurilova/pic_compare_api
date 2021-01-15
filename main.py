# from PIL import Image
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.secret_key = "dubdub"

@app.route('/')
def homepage():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    