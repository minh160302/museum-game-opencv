from flask import Flask, request, send_file
import base64
import io
from PIL import Image
import cv2
import numpy as np
import json
from image_processing import feature_matching
import boto3
from os import environ

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"


@app.route('/hello', methods=['POST'])
def upload():
    data = request.stream.read()
    data = base64.encodebytes(data)
    image = Image.open(io.BytesIO(base64.decodebytes(data)))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Encode image back to base64 string
    is_success, buffer = cv2.imencode(".jpeg", img)
    io_buf = io.BytesIO(buffer)
    io_buf.seek(0)

    return send_file(io_buf, mimetype="image/jpeg")


@app.route('/feature_matching', methods=['POST'])
def match():
    data = request.stream.read()
    data = base64.encodebytes(data)
    image = Image.open(io.BytesIO(base64.decodebytes(data)))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    bucket = boto3.resource(
        "s3",
        aws_access_key_id=environ.get('aws_access_key_id'),
        aws_secret_access_key=environ.get('aws_secret_access_key')
    ).Bucket("source-image-bucket")
    file_stream = io.BytesIO()
    bucket.Object("JoshuaSun_Martin.jpg").download_fileobj(file_stream)
    np_1d_array = np.frombuffer(file_stream.getbuffer(), dtype="uint8")
    sample_img = cv2.imdecode(np_1d_array, cv2.IMREAD_COLOR)

    cnt_match = feature_matching(img, sample_img)
    response = app.response_class(
        response=json.dumps({"count": cnt_match}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/health')
def health():
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
