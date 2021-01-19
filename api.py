from PIL import Image
from fastapi import FastAPI, Request, HTTPException
from imgcompare import image_diff_percent
import requests
from io import BytesIO
from pydantic import BaseModel
import urllib

class Payload(BaseModel):
    image1: str
    image2: str
    api_key: str

app = FastAPI()
# since it's a test I'm hardcoding but must be passed in ENV
secret_key = "kmrhn74zgzcq4nqb"

def save(url):
    """Save file and return its name"""
    filename = url.split("/")[-1]
    urllib.request.urlretrieve(url, filename)
    return filename

def download(urls):
    """Download images from given URLs, return a list of their names"""
    return list(map(save, urls))

def compare(filenames):
    """Compare two given images, return difference percentage"""
    filename1, filename2 = filenames
    return round(image_diff_percent(filename1, filename2),2)

def authorize(api_key):
    """Check authorization key"""
    if api_key != secret_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post('/api/compare')
def index(links: Payload):
    """Take POST request and send a response (image diff percentage)"""
    authorize(links.api_key)
    files = download([links.image1, links.image2])
    return {"percent_difference" : compare(files)}

