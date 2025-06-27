import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check for valid file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return '<h1>About Page</h1>'

# Contact page
@app.route('/contact')
def contact():
    return '<h1>Contact Page</h1>'

# Prediction page (GET for form, POST for result)
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('prediction.html', prediction="No file part", image_url=None)

        file = request.files['image']
        if file.filename == '':
            return render_template('prediction.html', prediction="No selected file", image_url=None)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Dummy prediction 
            predicted_class = "Hibiscus Pollen Grain"

            return render_template('prediction.html',
                                   prediction=predicted_class,
                                   image_url=url_for('static', filename='uploads/' + filename))
        else:
            return render_template('prediction.html', prediction="Invalid file type.", image_url=None)

    # GET request
    return render_template('prediction.html', prediction="", image_url=None)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
