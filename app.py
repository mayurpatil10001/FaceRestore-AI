import os
import replicate
import requests
import zipfile
import shutil
import base64
import uuid  # Ensure this is imported
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import time

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key-123'  # For flash messages
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size: 16MB

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Load environment variables
load_dotenv()
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        # Check if files were uploaded
        if 'images' not in request.files:
            flash('No files selected!')
            return redirect(request.url)
        
        files = request.files.getlist('images')
        if not files or len(files) > 20:
            flash('Please upload between 1 and 20 images.')
            return redirect(request.url)

        # Create a unique folder for this session
        session_id = str(uuid.uuid4())  # Fixed: Call uuid4() to generate UUID
        session_upload_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        session_output_path = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        os.makedirs(session_upload_path, exist_ok=True)
        os.makedirs(session_output_path, exist_ok=True)

        # Save uploaded files
        uploaded_filenames = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(session_upload_path, filename))
                uploaded_filenames.append(filename)
            else:
                flash(f'Invalid file: {file.filename}. Only PNG, JPG, JPEG allowed.')
                return redirect(request.url)

        # Process images with GFPGAN
        enhanced_files = []
        for filename in uploaded_filenames:
            file_path = os.path.join(session_upload_path, filename)
            try:
                # Read and encode image to base64 for Replicate API
                with open(file_path, 'rb') as f:
                    data = base64.b64encode(f.read()).decode('utf-8')
                    img_data_uri = f"data:image/jpeg;base64,{data}"

                # Run GFPGAN model
                input_data = {"img": img_data_uri}
                prediction = replicate.predictions.create(
                    version="0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
                    input=input_data
                )

                # Poll for prediction completion
                while prediction.status not in ['succeeded', 'failed', 'canceled']:
                    time.sleep(2)  # Wait before polling
                    prediction.reload()

                if prediction.status == 'succeeded':
                    # Download enhanced image
                    output_url = prediction.output
                    output_filename = f"enhanced_{filename}"
                    output_path = os.path.join(session_output_path, output_filename)
                    response = requests.get(output_url)
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    enhanced_files.append(output_filename)
                else:
                    flash(f'Failed to process {filename}.')
            except Exception as e:
                flash(f'Error processing {filename}: {str(e)}')
                continue

        if not enhanced_files:
            flash('No images were processed successfully.')
            return redirect(request.url)

        # Create a zip file of enhanced images
        zip_filename = f'enhanced_images_{session_id}.zip'
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in enhanced_files:
                file_path = os.path.join(session_output_path, filename)
                zipf.write(file_path, filename)

        # Clean up temporary files
        shutil.rmtree(session_upload_path)
        if len(enhanced_files) < len(uploaded_filenames):
            shutil.rmtree(session_output_path, ignore_errors=True)

        # Send zip file to user
        return send_file(zip_path, as_attachment=True, download_name='enhanced_images.zip')

    # Render upload form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)