import os
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter, ImageOps
import io

app = Flask(__name__)

def convert_to_sketch(image):
    gray = ImageOps.grayscale(image)
    edge = gray.filter(ImageFilter.FIND_EDGES)
    return edge

@app.route("/convert", methods=["POST"])
def convert():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    image_file = request.files["image"]
    image = Image.open(image_file.stream)
    sketch = convert_to_sketch(image)

    buf = io.BytesIO()
    sketch.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.route("/", methods=["GET"])
def home():
    return "Colorify Sketch API is running!"

# 👇 Bu satırı en sona ekle!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
