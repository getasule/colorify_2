
from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image, ImageOps, ImageFilter
import io

app = Flask(__name__)
CORS(app)

def cartoon_sketch(image):
    gray = ImageOps.grayscale(image)
    inverted = ImageOps.invert(gray)
    blurred = inverted.filter(ImageFilter.GaussianBlur(8))
    blended = Image.blend(gray, blurred, alpha=0.6)
    final = ImageOps.invert(blended)
    thresholded = final.point(lambda p: 255 if p > 140 else 0)
    return thresholded.convert('L')

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    file = request.files['image']
    image = Image.open(file.stream).convert('RGB')
    result = cartoon_sketch(image)
    buffer = io.BytesIO()
    result.save(buffer, format='PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

@app.route('/')
def index():
    return '🖼️ Colorify Sketch API is ready!'
