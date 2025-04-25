
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, ImageOps, ImageFilter
import io

app = Flask(__name__)
CORS(app)

def convert_to_sketch(image):
    # Daha yumuşak, temiz bir boyama kitabı efekti (blur + blend)
    gray = ImageOps.grayscale(image)
    inverted = ImageOps.invert(gray)
    blur = inverted.filter(ImageFilter.GaussianBlur(10))
    sketch = Image.blend(gray, blur, alpha=0.5)
    final = ImageOps.invert(sketch)
    return final

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    image_file = request.files['image']
    mode = request.form.get('mode', 'sketch')

    image = Image.open(image_file.stream)

    if mode == 'sketch':
        output = convert_to_sketch(image)
    else:
        return jsonify({'error': f'Unknown mode: {mode}'}), 400

    buf = io.BytesIO()
    output.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/')
def home():
    return 'Colorify Advanced API is live!'
