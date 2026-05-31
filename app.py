from flask import Flask, render_template, request, send_from_directory
import cv2
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def pencil_sketch(input_path, output_path):
    img = cv2.imread(input_path)
    img = cv2.resize(img, (600, 400))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    inv_blur = cv2.bitwise_not(blur)

    sketch = cv2.divide(gray, inv_blur, scale=256.0)

    cv2.imwrite(output_path, sketch)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]

        filename = "sketch_output.png"

        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        file.save(input_path)

        pencil_sketch(input_path, output_path)

        result = filename

    return render_template("index.html", result=result)


# ✅ download route (FIXED)
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        OUTPUT_FOLDER,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)