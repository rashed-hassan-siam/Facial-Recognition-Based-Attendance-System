from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'images/Group'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = "group_image.jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('result'))

@app.route('/result')
def result():
    exec(open("Face_Recognition.py").read())
     # Execute the Bash script and capture its output
    result = subprocess.run('./list-devices.sh', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    return render_template('result.html', output=output)

@app.route('/image')
def get_image():
    # Assuming the image is stored in a folder named "images"
    return send_from_directory('images/Group', 'output.jpg')

if __name__ == '__main__':
    app.run(debug=True)
