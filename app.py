import os
import tempfile
from flask import Flask, request, jsonify
from gradio_client import Client, handle_file

app = Flask(__name__)
client = Client("malavikaaaaaaaaaaaaaaaaaaa/facerec")

@app.route('/add_face', methods=['POST'])
def add_face():
    try:
        print("Form keys:", list(request.form.keys()))
        print("File keys:", list(request.files.keys()))

        if 'name' not in request.form or 'image' not in request.files:
            return jsonify({"status": "error", "message": "Missing 'name' or 'image' in form-data"}), 400

        name = request.form.get('name')
        img_file = request.files['image']

        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            img_file.save(temp_file)
            temp_file_path = temp_file.name

        result = client.predict(
            name=name,
            img=handle_file(temp_file_path),
            api_name="/add_face"
        )

        # Delete temp file
        os.remove(temp_file_path)

        return jsonify({"status": "success", "result": result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500





@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "Missing 'image' in form-data"}), 400

        img_file = request.files['image']

        temp_path = f"temp_{img_file.filename}"
        img_file.save(temp_path)

        result = client.predict(
            img=handle_file(temp_path),
            api_name="/recognize_face"
        )

        os.remove(temp_path)

        return jsonify({"status": "success", "result": result})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
