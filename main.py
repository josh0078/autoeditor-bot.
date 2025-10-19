from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_video():
    input_path = f"input_{uuid.uuid4().hex}.mp4"
    output_path = f"output_{uuid.uuid4().hex}.mp4"
    file = request.files['data']
    file.save(input_path)

    subprocess.run([
        "auto-editor", input_path,
        "--remove-silence",
        "--min-silence-length", "0.6",
        "--silence-threshold", "0.03",
        "-o", output_path
    ])

    response = send_file(output_path, mimetype='video/mp4')
    os.remove(input_path)
    os.remove(output_path)
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
