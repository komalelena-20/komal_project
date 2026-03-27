from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_data):
    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    return ''.join(chars)

def encode_image(img, secret_text):
    secret_text += "#####"
    binary_data = text_to_binary(secret_text)
    data_len = len(binary_data)

    pixels = list(img.getdata())
    if data_len > len(pixels) * 3:
        raise ValueError("Message too long for this image.")

    new_pixels = []
    data_index = 0
    for pixel in pixels:
        r, g, b = pixel
        if data_index < data_len:
            r = (r & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < data_len:
            g = (g & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < data_len:
            b = (b & ~1) | int(binary_data[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    return img

def decode_image(img):
    pixels = list(img.getdata())
    binary_data = ''
    
    for pixel in pixels:
        for color in pixel[:3]:  # r, g, b
            binary_data += str(color & 1)

    text = binary_to_text(binary_data)
    secret_message = text.split('#####')[0]  # Stop at delimiter
    return secret_message

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        img_file = request.files['image']
        secret_text = request.form['secret']
        img = Image.open(img_file).convert('RGB') # type: ignore
        encoded_img = encode_image(img, secret_text)

        buffer = io.BytesIO()
        encoded_img.save(buffer, format="PNG")
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='encoded_image.png', mimetype='image/png')

    return render_template('index.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        img_file = request.files['image']
        img = Image.open(img_file).convert('RGB') # type: ignore
        secret_message = decode_image(img)
        return render_template('decode.html', secret=secret_message)

    return render_template('decode.html', secret=None)

if __name__ == '__main__':
    app.run(debug=True)
