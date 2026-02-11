from flask import Flask, render_template, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'C:/Users/cmazz/PycharmProjects/UntitledAssitantTool/sources'  # Set your uploads directory
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Limit for total data is 10 MB
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')  # The HTML file will contain your image and the upload area


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)

    files = request.files.getlist('files[]')

    filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
        else:
            flash('Allowed file types are PDFs')

    return render_template('index.html', filenames=filenames)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/ask_question')
def ask_question():
    # Redirect to the question-asking page
    return render_template('ask_question.html')


if __name__ == '__main__':
    app.run(debug=False)
