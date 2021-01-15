from PIL import Image
from flask import Flask, render_template, jsonify, request
import requests
from io import BytesIO
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = "123"

@app.before_request
def authorize():
    """Read auth-key from header and return 401 if auth fails"""
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {app.secret_key}":
        abort(
            401,"Unauthorized access",
        )
    
@app.route('/')
def homepage():
    return render_template("index.html")

def parse():
    """Parse data from the client"""
    images = request.get_json()
    image_one_url = images["image_one"]
    image_two_url = images["image_two"]
    if not image_one_url or not image_two_url:
        abort(
            400, "Bad Request"
        )
    return [image_one_url, image_two_url]

def download(urls):
    """Download images from url"""
    responses = map(requests.get, urls)
    if any(not r.ok for r in responses):
        abort(
            400, "Bad Request"
        )
    images = map(lambda r: Image.open(BytesIO(r.content)), responses)
    return images

def compare(images):
    """Compare two given images and return similarity percentage"""
    i1, i2 = images
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
    ncomponents = i1.size[0] * i1.size[1] * 3
    difference = round((dif / 255.0 * 100 / ncomponents), 2)
    result = 100-difference
    return result

@app.route('/api/compare.json', methods=["POST"])
def compare_two_pictures():
    """Return pictures similarity data back to the client"""
    urls = parse()
    images = download(urls)
    result = compare(images)
    return jsonify({"result" : result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    