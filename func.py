from flask import Flask, render_template, request
import cv2
import time

app = Flask(__name__)


def increase_resolution(image_path):
    img = cv2.imread(image_path)

    width = img.shape[1]
    height = img.shape[0]
    bicubic = cv2.resize(img, (width*4, height*4))

    super_res = cv2.dnn_superres.DnnSuperResImpl_create()

    super_res.readModel('ESPCN_x4.pb')
    super_res.setModel('espcn', 4)
    espcn_image = super_res.upsample(img)

    super_res.readModel('FSRCNN_x4.pb')
    super_res.setModel('fsrcnn', 4)
    fsrcnn_image = super_res.upsample(img)
    # Apply the algorithm to increase the resolution
    # You would need to define the algorithm that suits your purpose

    # Return the high-resolution image
    return fsrcnn_image


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's input (the low-resolution image)
        low_res_img = request.files['low_res_img'].read()

        # Apply the algorithm to increase the resolution
        high_res_img = increase_resolution(low_res_img)

        # Return the high-resolution image to the user
        return render_template('result.html', high_res_img=high_res_img)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

