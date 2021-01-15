from PIL import Image
import requests
from io import BytesIO

image_one = input("Enter image 1 URL")
image_two = input("Enter image 2 URL")
# i1 = request.form['image_one']
# i2 = request.form['image_two']

# i1 = Image.open("image1.png")
# i2 = Image.open("image2.png")

response1 = requests.get(image_one)
response2 = requests.get(image_two)

i1 = Image.open(BytesIO(response1.content))
i2 = Image.open(BytesIO(response2.content))

# assert i1.mode == i2.mode, "Different kinds of images."
# assert i1.size == i2.size, "Different sizes."

pairs = zip(i1.getdata(), i2.getdata())
if len(i1.getbands()) == 1:
    # for gray-scale jpegs
    dif = sum(abs(p1-p2) for p1,p2 in pairs)
else:
    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

ncomponents = i1.size[0] * i1.size[1] * 3
# return ( { "result" : dif / 255.0 * 100 / ncomponents} )
print(f"Difference is {round((dif / 255.0 * 100 / ncomponents), 2)}%")