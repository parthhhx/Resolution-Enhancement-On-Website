from flask import Flask, request, jsonify
from PIL import Image
import io
import cv2
import time

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert_image():
    # Get the uploaded low-resolution image from the request
    file = request.files['image']
    img = Image.open(file)

    width = img.shape[1]
    height = img.shape[0]
    bicubic = cv2.resize(img, (width*4, height*4))
    # Call your Python function to generate a high-resolution image
    # high_res_img = generate_high_resolution_image(img)

    # Convert the high-resolution image to bytes for sending back in the response

    super_res = cv2.dnn_superres.DnnSuperResImpl_create()
    super_res.readModel('ESPCN_x4.pb')
    super_res.setModel('espcn', 4)
    espcn_image = super_res.upsample(img)

    super_res.readModel('FSRCNN_x4.pb')
    super_res.setModel('fsrcnn', 4)
    high_res_img_bytes = super_res.upsample(img)

    high_res_img_bytes = io.BytesIO()
    high_res_img_bytes.save(high_res_img_bytes, format='PNG')
    high_res_img_bytes.seek(0)

    # Send the high-resolution image back in the response
    return jsonify({'image': high_res_img_bytes.read().decode('latin-1')})


if __name__ == '__main__':
    app.run()
