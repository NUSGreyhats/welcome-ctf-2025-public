from flask import Flask, request, render_template_string, redirect, url_for, send_file, Response
import socket
import string
import random
import os
import html

app = Flask(__name__)

uploaded_images = {}

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def notify_admin(image_id):
    try:
        admin_host = os.getenv('ADMIN_HOST', 'localhost')
        admin_port = int(os.getenv('ADMIN_PORT', '3001'))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((admin_host, admin_port))
            s.send(image_id.encode())
    except Exception as e:
        print(f"Failed to notify admin: {e}")

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Image Gallery</title>
</head>
<body>
    <h1>Upload Your Image</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="image" accept=".jpg,.jpeg,.svg" required><br><br>
        <input type="submit" value="Upload Image">
    </form>
    <p><small>Supported formats: JPG, SVG only</small></p>
    <p><small>Note: An admin will review your upload automatically.</small></p>
</body>
</html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['image']
    if not file.filename:
        return redirect(url_for('index'))
    
    filename = file.filename.lower()
    if not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.svg')):
        return "Only JPG and SVG files allowed", 400
    
    content = file.read()
    if len(content) > 50000:
        return "File too large", 400
    
    content_type = 'image/jpeg' if filename.endswith(('.jpg', '.jpeg')) else 'image/svg+xml'
    
    image_id = generate_id()
    uploaded_images[image_id] = {
        'content': content,
        'filename': file.filename,
        'content_type': content_type
    }
    
    notify_admin(image_id)
    
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head>
    <title>Upload Successful</title>
</head>
<body>
    <h1>Upload Successful!</h1>
    <p>Your image ID is: <strong>{html.escape(image_id)}</strong></p>
    <p>An admin will review it shortly.</p>
    <p><a href="/{html.escape(image_id)}">View your image</a></p>
    <p><a href="/">Upload another image</a></p>
</body>
</html>
    ''')

@app.route('/<image_id>')
def view_image(image_id):
    if image_id not in uploaded_images:
        return "Image not found", 404
    
    image_data = uploaded_images[image_id]
    
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head>
    <title>View Image</title>
</head>
<body>
    <h1>Image: {html.escape(image_id)}</h1>
    <div>
        <img src="/image/{html.escape(image_id)}" style="max-width: 500px;">
    </div>
    <p>Filename: {html.escape(image_data['filename'])}</p>
    <p><a href="/">Upload another image</a></p>
</body>
</html>
    ''')

@app.route('/image/<image_id>')
def serve_image(image_id):
    if image_id not in uploaded_images:
        return "Image not found", 404
    
    image_data = uploaded_images[image_id]
    return Response(
        image_data['content'],
        mimetype=image_data['content_type']
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)